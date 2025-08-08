"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Download, CheckCircle, RotateCcw, AlertTriangle } from "lucide-react"
import { StepNavigation } from "@/components/step-navigation"
import { toast } from "sonner"
import { useExamStore } from "@/lib/store"

interface FinalResult {
  stt: number
  mssv: string
  hoTen: string
  maDe: string
  diem: number
}

export default function Step5Page() {
  const router = useRouter()
  const { examResults, studentFile } = useExamStore()
  const [isExporting, setIsExporting] = useState(false)
  const [finalResults, setFinalResults] = useState<FinalResult[]>([])

  // Function to convert score to 10-point scale
  const convertToTenPointScale = (correctAnswers: number, totalQuestions: number): number => {
    if (totalQuestions === 0) return 0
    return (correctAnswers / totalQuestions) * 10
  }

  // Convert examResults to finalResults format
  useEffect(() => {
    if (examResults && examResults.length > 0) {
      const convertedResults: FinalResult[] = examResults.map((result, index) => {
        const correctAnswers = result.score || 0  // Backend trả về số câu đúng trong field score
        const totalQuestions = result.numQuestions || 0
        const tenPointScore = convertToTenPointScale(correctAnswers, totalQuestions)
        
        return {
          stt: index + 1,
          mssv: result.id || result.recognizedStudentId || 'N/A',
          hoTen: result.name || 'N/A',
          maDe: result.recognizedExamCode || result.testVariant || 'N/A',
          diem: tenPointScore  // Điểm thang 10
        }
      })
      setFinalResults(convertedResults)
      console.log('📊 Step-5: Converted exam results:', convertedResults)
      console.log('📊 Step-5: Raw exam results sample:', examResults[0])
      console.log('📊 Step-5: Available fields:', examResults[0] ? Object.keys(examResults[0]) : 'No data')
    } else {
      console.log('⚠️  Step-5: No exam results found')
      setFinalResults([])
    }
  }, [examResults])

  const handleExport = async () => {
    if (!finalResults || finalResults.length === 0) {
      toast.error("Không có dữ liệu để xuất file")
      return
    }

    if (!studentFile) {
      toast.error("Không tìm thấy file danh sách sinh viên gốc")
      return
    }

    setIsExporting(true)

    try {
      // Prepare data for API
      const exportData = {
        results: finalResults.map((result, index) => {
          const examResult = examResults?.[index]
          return {
            stt: result.stt,
            mssv: result.mssv,
            hoTen: result.hoTen,
            maDe: result.maDe,
            diem: result.diem, // Điểm thang 10
            cauDung: examResult?.score || 0,
            tongCau: examResult?.numQuestions || 0
          }
        }),
        student_filename: studentFile.name
      }

      console.log('📤 Exporting data:', exportData)

      // Call API to export to original Excel
      const response = await fetch('http://localhost:5000/api/export_to_original_excel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(exportData),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.error || 'Failed to export to Excel')
      }

      console.log('📤 Export result:', result)

      // Download the generated file
      const downloadResponse = await fetch(`http://localhost:5000/api/download_result_excel/${result.filename}`)
      
      if (!downloadResponse.ok) {
        throw new Error('Failed to download exported file')
      }

      const blob = await downloadResponse.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = result.filename
      link.style.display = 'none'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

      toast.success(`Đã xuất kết quả vào file Excel gốc với đầy đủ format! (${result.updated_count}/${result.total_students} sinh viên)`)
      
      // Log thông tin chi tiết
      if (result.mssv_column && result.thangdiem4_column) {
        console.log(`📊 Updated columns - MSSV: column ${result.mssv_column}, ThangDiem4: column ${result.thangdiem4_column}`)
      }
    } catch (error) {
      console.error('Export error:', error)
      toast.error("Có lỗi xảy ra khi xuất file: " + (error instanceof Error ? error.message : 'Unknown error'))
    } finally {
      setIsExporting(false)
    }
  }

  const handleNewExam = () => {
    router.push("/exam/step-1")
  }

  const handleHome = () => {
    router.push("/")
  }

  const averageScore = finalResults.length > 0 
    ? finalResults.reduce((sum, result) => sum + result.diem, 0) / finalResults.length 
    : 0

  // Show message if no data
  if (!finalResults || finalResults.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <StepNavigation currentStep={5} />
          
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-green-600" />
                Bước 5: Xuất Kết Quả
              </CardTitle>
              <CardDescription>
                Chưa có dữ liệu kết quả để hiển thị.
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <Alert className="border-yellow-200 bg-yellow-50">
                <AlertTriangle className="h-4 w-4 text-yellow-600" />
                <AlertDescription className="text-yellow-800">
                  Chưa có kết quả chấm thi nào. Vui lòng quay lại các bước trước để xử lý bài thi.
                </AlertDescription>
              </Alert>
              
              <div className="flex justify-between">
                <Button variant="outline" onClick={handleHome}>
                  Về Trang Chủ
                </Button>
                <Button onClick={() => router.push("/exam/step-1")} className="flex items-center gap-2">
                  <RotateCcw className="w-4 h-4" />
                  Bắt Đầu Lại
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <StepNavigation currentStep={5} />

        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="w-6 h-6 text-green-600" />
              Bước 5: Xuất Kết Quả
            </CardTitle>
            <CardDescription>
              Quá trình chấm điểm đã hoàn tất. Xem lại kết quả cuối cùng và tải xuống file Excel.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            <Alert className="border-green-200 bg-green-50">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800">
                <strong>Hoàn tất!</strong> Quá trình chấm điểm đã kết thúc thành công. Đã xử lý {finalResults.length}{" "}
                bài thi với điểm trung bình {averageScore.toFixed(1)}.
              </AlertDescription>
            </Alert>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-blue-600">{finalResults.length}</div>
                <div className="text-sm text-blue-800">Tổng số bài</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-green-600">
                  {finalResults.filter((r) => r.diem >= 5).length}
                </div>
                <div className="text-sm text-green-800">Đạt (≥5.0)</div>
              </div>
              <div className="bg-red-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-red-600">{finalResults.filter((r) => r.diem < 5).length}</div>
                <div className="text-sm text-red-800">Không đạt (&lt;5.0)</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-purple-600">{averageScore.toFixed(1)}</div>
                <div className="text-sm text-purple-800">Điểm TB</div>
              </div>
            </div>

            {/* Results Table */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Bảng kết quả cuối cùng:</h3>
              <div className="border rounded-lg overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-16">STT</TableHead>
                      <TableHead>MSSV</TableHead>
                      <TableHead>Họ và Tên</TableHead>
                      <TableHead>Mã Đề</TableHead>
                      <TableHead>Câu đúng</TableHead>
                      <TableHead>Điểm</TableHead>
                      <TableHead>Kết Quả</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {finalResults.map((result, index) => {
                      const examResult = examResults?.[index]
                      return (
                        <TableRow key={result.stt}>
                          <TableCell>{result.stt}</TableCell>
                          <TableCell className="font-mono">{result.mssv}</TableCell>
                          <TableCell>{result.hoTen}</TableCell>
                          <TableCell className="font-mono">{result.maDe}</TableCell>
                          <TableCell>
                            <span className="font-semibold">
                              {examResult?.score || 0}/{examResult?.numQuestions || 0}
                            </span>
                          </TableCell>
                          <TableCell>
                            <span
                              className={`font-semibold ${
                                result.diem >= 8 ? "text-green-600" : result.diem >= 5 ? "text-blue-600" : "text-red-600"
                              }`}
                            >
                              {result.diem.toFixed(1)}
                            </span>
                          </TableCell>
                          <TableCell>
                            <span
                              className={`px-2 py-1 rounded-full text-xs font-medium ${
                                result.diem >= 5 ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                              }`}
                            >
                              {result.diem >= 5 ? "Đạt" : "Không đạt"}
                            </span>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </div>
            </div>

            {/* Export Section */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Xuất kết quả vào file Excel gốc</h3>
                  <p className="text-gray-500 text-sm">
                    File: {studentFile?.name || 'Không có file'}
                  </p>
                </div>
                <Button onClick={handleExport} disabled={isExporting || !studentFile} size="lg" className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white">
                  {isExporting ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  ) : (
                    <Download className="w-4 h-4" />
                  )}
                  {isExporting ? "Đang xuất..." : "Tải xuống File Kết Quả (Excel)"}
                </Button>
              </div>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={handleHome}>
                Về Trang Chủ
              </Button>
              <Button onClick={handleNewExam} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white">
                <RotateCcw className="w-4 h-4" />
                Tạo Kỳ Thi Mới
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
