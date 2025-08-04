"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Download, CheckCircle, RotateCcw } from "lucide-react"
import { StepNavigation } from "@/components/step-navigation"
import { toast } from "sonner"

interface FinalResult {
  stt: number
  mssv: string
  hoTen: string
  maDe: string
  diem: number
}

export default function Step5Page() {
  const router = useRouter()
  const [isExporting, setIsExporting] = useState(false)

  const finalResults: FinalResult[] = [
    { stt: 1, mssv: "20181234", hoTen: "Nguyễn Văn An", maDe: "132", diem: 8.5 },
    { stt: 2, mssv: "20181235", hoTen: "Trần Thị Bình", maDe: "209", diem: 6.0 },
    { stt: 3, mssv: "20181236", hoTen: "Lê Văn Cường", maDe: "357", diem: 7.0 },
  ]

  const handleExport = async () => {
    setIsExporting(true)

    try {
      // Simulate file generation
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Create a mock Excel file download
      const csvContent = [
        "STT,MSSV,Họ và Tên,Mã Đề,Điểm",
        ...finalResults.map((result) => `${result.stt},${result.mssv},${result.hoTen},${result.maDe},${result.diem}`),
      ].join("\n")

      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
      const link = document.createElement("a")
      const url = URL.createObjectURL(blob)
      link.setAttribute("href", url)
      link.setAttribute("download", `ket-qua-thi-${new Date().toISOString().split("T")[0]}.csv`)
      link.style.visibility = "hidden"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      toast.success("Đã tải xuống file kết quả thành công!")
    } catch (error) {
      toast.error("Có lỗi xảy ra khi xuất file")
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

  const averageScore = finalResults.reduce((sum, result) => sum + result.diem, 0) / finalResults.length

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
                      <TableHead>Điểm</TableHead>
                      <TableHead>Kết Quả</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {finalResults.map((result) => (
                      <TableRow key={result.stt}>
                        <TableCell>{result.stt}</TableCell>
                        <TableCell className="font-mono">{result.mssv}</TableCell>
                        <TableCell>{result.hoTen}</TableCell>
                        <TableCell className="font-mono">{result.maDe}</TableCell>
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
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>

            {/* Export Section */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Xuất file kết quả</h3>
                  <p className="text-gray-600">Tải xuống file Excel chứa đầy đủ kết quả chấm thi</p>
                </div>
                <Button onClick={handleExport} disabled={isExporting} size="lg" className="flex items-center gap-2">
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
              <Button onClick={handleNewExam} className="flex items-center gap-2">
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
