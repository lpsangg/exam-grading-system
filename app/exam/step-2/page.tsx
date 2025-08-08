"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Users, CheckCircle, AlertCircle } from "lucide-react"
import { useExamStore } from "@/lib/store"
import { StepNavigation } from "@/components/step-navigation"
import { FileUpload } from "@/components/file-upload"
import { toast } from "sonner"

interface Student {
  stt: number
  mssv: string
  hoTen: string
}

export default function Step2Page() {
  const router = useRouter()
  const { setStudentFile, studentFile, setStudentCount, setCalculatedRooms } = useExamStore()
  const [isUploading, setIsUploading] = useState(false)
  const [students, setStudents] = useState<Student[]>([])
  const [uploadResult, setUploadResult] = useState<{
    success: boolean
    message: string
    studentCount?: number
  } | null>(null)

  const handleFileUpload = async (file: File) => {
    if (!file.name.endsWith(".xlsx")) {
      toast.error("Vui lòng chọn file Excel (.xlsx)")
      return
    }

    setIsUploading(true)

    try {
      // Gọi API FastAPI thực tế
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch('http://localhost:5000/api/upload_student_list', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      
      if (res.ok) {
        setStudentFile(file)
        setStudents(data.students || [])
        setStudentCount(data.studentCount || 0)
        
        // Tính toán phòng thi dựa trên số lượng sinh viên
        const roomResponse = await fetch('http://localhost:5000/api/calculate_rooms', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_count: data.studentCount || 0 }),
        });
        
        if (roomResponse.ok) {
          const roomData = await roomResponse.json();
          setCalculatedRooms(roomData.rooms || []);
        }
        
        setUploadResult({
        success: true,
          message: data.message,
          studentCount: data.studentCount || 0,
        })
      toast.success("Tải lên danh sách sinh viên thành công!")
      } else {
        setUploadResult({ 
          success: false, 
          message: data.error || 'Lỗi không xác định' 
        })
        toast.error(data.error || "Có lỗi xảy ra khi tải file")
      }
    } catch (error) {
      setUploadResult({ 
        success: false,
        message: "Định dạng file không hợp lệ hoặc không có dữ liệu sinh viên." 
      })
      toast.error("Có lỗi xảy ra khi tải file")
    } finally {
      setIsUploading(false)
    }
  }

  const handleNext = () => {
    router.push("/exam/step-3")
  }

  const handleBack = () => {
    router.push("/exam/step-1")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-3 sm:px-6 py-4 sm:py-8">
        <StepNavigation currentStep={2} />

        <Card className="mt-4 sm:mt-8">
          <CardHeader className="pb-4 sm:pb-6">
            <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
              <Users className="w-5 h-5 sm:w-6 sm:h-6" />
              Bước 2: Tải Lên Danh Sách Lớp
            </CardTitle>
            <CardDescription className="text-sm sm:text-base">
              Tải lên file Excel chứa danh sách sinh viên. File phải có định dạng .xlsx
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4 sm:space-y-6">
            <FileUpload
              onFileSelect={handleFileUpload}
              accept=".xlsx"
              disabled={isUploading}
              title="Kéo thả file danh sách sinh viên vào đây hoặc click để chọn"
              description="Chỉ chấp nhận file Excel (.xlsx)"
            />

            {isUploading && (
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span className="text-sm">Đang xử lý file...</span>
              </div>
            )}

            {uploadResult && (
              <Alert className={uploadResult.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}>
                {uploadResult.success ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-600" />
                )}
                <AlertDescription className={`${uploadResult.success ? "text-green-800" : "text-red-800"} text-sm sm:text-base`}>
                  {uploadResult.message}
                  {uploadResult.studentCount && (
                    <div className="mt-1">
                      <strong>Số lượng sinh viên:</strong> {uploadResult.studentCount}
                    </div>
                  )}
                </AlertDescription>
              </Alert>
            )}

            {students.length > 0 && (
              <div className="space-y-3 sm:space-y-4">
                <h3 className="text-base sm:text-lg font-semibold">Xem trước danh sách sinh viên:</h3>
                <div className="border rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="w-16 text-xs sm:text-sm">STT</TableHead>
                          <TableHead className="text-xs sm:text-sm">MSSV</TableHead>
                          <TableHead className="text-xs sm:text-sm">Họ và Tên</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {students.slice(0, 5).map((student) => (
                          <TableRow key={student.stt}>
                            <TableCell className="text-xs sm:text-sm">{student.stt}</TableCell>
                            <TableCell className="font-mono text-xs sm:text-sm">{student.mssv}</TableCell>
                            <TableCell className="text-xs sm:text-sm">{student.hoTen}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </div>
                {students.length > 5 && (
                  <p className="text-xs sm:text-sm text-gray-600 text-center">
                    Hiển thị 5 sinh viên đầu tiên. Tổng cộng: {students.length} sinh viên
                  </p>
                )}
              </div>
            )}

            <div className="flex flex-col sm:flex-row justify-between gap-3 sm:gap-0">
              <Button variant="outline" onClick={handleBack} className="w-full sm:w-auto">
                Quay Lại
              </Button>
              <Button onClick={handleNext} disabled={!uploadResult?.success} className="w-full sm:w-auto">
                Tiếp Tục
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
