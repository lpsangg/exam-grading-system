"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { BarChart3, Edit, CheckCircle, AlertTriangle, Eye } from "lucide-react"
import { StepNavigation } from "@/components/step-navigation"
import { toast } from "sonner"
import Image from "next/image"
import { useExamStore } from "@/lib/store"

interface ExamResult {
  id: string
  imageName: string
  recognizedStudentId: string
  recognizedExamCode: string
  score: number
  status: "success" | "warning" | "error"
  imageUrl: string
  name?: string
  indexStudent?: string
  answers?: string[]
  numQuestions?: number
}

export default function Step4Page() {
  const router = useRouter()
  const { examResults, setExamResults, examCodes, studentList } = useExamStore()
  const [results, setResults] = useState<ExamResult[]>([])

  // Đồng bộ results với examResults từ store
  useEffect(() => {
    if (examResults && examResults.length > 0) {
      console.log('📊 Step-4: Received examResults:', examResults)
      setResults(examResults)
    }
  }, [examResults])

  // Debug log khi results thay đổi
  useEffect(() => {
    console.log('📊 Step-4: Current results state:', results)
  }, [results])

  // Nếu không có dữ liệu thực, chuyển hướng về step-3
  useEffect(() => {
    console.log('📊 Step-4: Checking examResults for redirect:', examResults)
    if (!examResults || examResults.length === 0) {
      console.log('📊 Step-4: No data, redirecting to step-3')
      router.push("/exam/step-3")
    }
  }, [examResults, router])

  const [editingResult, setEditingResult] = useState<ExamResult | null>(null)
  const [editForm, setEditForm] = useState({
    studentId: "",
    examCode: "",
    name: "",
  })

  const handleEdit = (result: ExamResult) => {
    setEditingResult(result)
    setEditForm({
      studentId: result.recognizedStudentId,
      examCode: result.recognizedExamCode,
      name: result.name || "",
    })
  }

  const handleSaveEdit = async () => {
    if (!editingResult) return

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Update the result
      setResults((prev) =>
        prev.map((result) =>
          result.id === editingResult.id
            ? {
                ...result,
                recognizedStudentId: editForm.studentId,
                recognizedExamCode: editForm.examCode,
                name: editForm.name,
                status: "success", // Assuming mockStudents is removed, so always success for now
              }
            : result,
        ),
      )

      setEditingResult(null)
      toast.success("Đã cập nhật thông tin thành công!")
    } catch (error) {
      toast.error("Có lỗi xảy ra khi cập nhật")
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "success":
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Thành công</Badge>
      case "warning":
        return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Cảnh báo</Badge>
      case "error":
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Lỗi</Badge>
      default:
        return <Badge variant="secondary">Không xác định</Badge>
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "success":
        return <CheckCircle className="w-4 h-4 text-green-600" />
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />
      case "error":
        return <AlertTriangle className="w-4 h-4 text-red-600" />
      default:
        return null
    }
  }

  const handleNext = () => {
    router.push("/exam/step-5")
  }

  const handleBack = () => {
    router.push("/exam/step-3")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <StepNavigation currentStep={4} />

        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-6 h-6" />
              Bước 4: Xem Lại & Chỉnh Sửa
            </CardTitle>
            <CardDescription>Kiểm tra kết quả chấm sơ bộ và chỉnh sửa các lỗi nhận dạng nếu cần</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {!results || results.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">Đang tải dữ liệu...</p>
                <p className="text-sm text-gray-400 mt-2">
                  examResults: {examResults?.length || 0} items, 
                  results: {results?.length || 0} items
                </p>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="font-semibold text-green-800">Thành công</span>
                </div>
                <p className="text-2xl font-bold text-green-600 mt-1">
                  {results.filter((r) => r.status === "success").length}
                </p>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-600" />
                  <span className="font-semibold text-yellow-800">Cần kiểm tra</span>
                </div>
                <p className="text-2xl font-bold text-yellow-600 mt-1">
                  {results.filter((r) => r.status === "warning").length}
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-blue-600" />
                  <span className="font-semibold text-blue-800">Tổng số</span>
                </div>
                <p className="text-2xl font-bold text-blue-600 mt-1">{results.length}</p>
              </div>
            </div>

            <div className="border rounded-lg overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ảnh Gốc</TableHead>
                    <TableHead>Tên Sinh Viên</TableHead>
                    <TableHead>MSSV</TableHead>
                    <TableHead>Mã Đề</TableHead>
                    <TableHead>STT</TableHead>
                    <TableHead>Điểm</TableHead>
                    <TableHead>Trạng Thái</TableHead>
                    <TableHead>Hành Động</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.map((result, idx) => (
                    <TableRow key={`${result.id}-${result.imageName}-${idx}`} className={result.status === "warning" ? "bg-yellow-50" : ""}>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(result.status)}
                          <span className="font-mono text-sm">{result.imageName}</span>
                        </div>
                      </TableCell>
                      <TableCell>{result.name || 'Chưa nhận diện'}</TableCell>
                      <TableCell className="font-mono">{result.recognizedStudentId}</TableCell>
                      <TableCell className="font-mono">{result.recognizedExamCode}</TableCell>
                      <TableCell>{result.indexStudent || 'N/A'}</TableCell>
                      <TableCell>
                        <span className="font-semibold">{result.score.toFixed(1)}</span>
                        {result.numQuestions && (
                          <span className="text-gray-500 text-sm ml-1">/{result.numQuestions}</span>
                        )}
                      </TableCell>
                      <TableCell>{getStatusBadge(result.status)}</TableCell>
                      <TableCell>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm" onClick={() => handleEdit(result)}>
                              <Eye className="w-4 h-4 mr-1" />
                              Xem & Sửa
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-4xl">
                            <DialogHeader>
                              <DialogTitle>Chỉnh sửa kết quả - {result.imageName}</DialogTitle>
                            </DialogHeader>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                              <div>
                                <h3 className="font-semibold mb-2">Ảnh bài làm:</h3>
                                <div className="border rounded-lg overflow-hidden">
                                  <Image
                                    src={result.imageUrl || "/placeholder.svg"}
                                    alt={result.imageName || `Bài thi của ${result.name || 'sinh viên'}`}
                                    width={400}
                                    height={500}
                                    className="w-full h-auto"
                                  />
                                </div>
                              </div>

                              <div className="space-y-4">
                                <div>
                                  <Label htmlFor="student-select">MSSV</Label>
                                  <Select
                                    value={editForm.studentId}
                                    onValueChange={(value) => {
                                      const selectedStudent = studentList.find(s => s.id === value)
                                      setEditForm((prev) => ({ 
                                        ...prev, 
                                        studentId: value,
                                        name: selectedStudent?.name || prev.name
                                      }))
                                    }}
                                  >
                                    <SelectTrigger>
                                      <SelectValue placeholder="Chọn sinh viên" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {studentList.map((student) => (
                                        <SelectItem key={student.id} value={student.id}>
                                          {student.id} - {student.name}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>

                                <div>
                                  <Label htmlFor="student-name">Tên Sinh Viên</Label>
                                  <div className="px-3 py-2 border rounded-md bg-gray-50 text-gray-700">
                                    {editForm.name || 'Chưa có tên'}
                                  </div>
                                </div>

                                <div>
                                  <Label htmlFor="exam-code-select">Mã Đề</Label>
                                  <Select
                                    value={editForm.examCode}
                                    onValueChange={(value) => setEditForm((prev) => ({ ...prev, examCode: value }))}
                                  >
                                    <SelectTrigger>
                                      <SelectValue placeholder="Chọn mã đề" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {examCodes.map((code) => (
                                        <SelectItem key={code} value={code}>
                                          Mã đề {code}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>

                                <div className="pt-4">
                                  <Button onClick={handleSaveEdit} className="w-full">
                                    <Edit className="w-4 h-4 mr-2" />
                                    Lưu Thay Đổi
                                  </Button>
                                </div>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={handleBack}>
                Quay Lại
              </Button>
              <Button onClick={handleNext}>Xác Nhận & Xuất File</Button>
            </div>
            </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
