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
  const { setStudentFile, studentFile, setStudentCount, setCalculatedRooms, setStudentList } = useExamStore()
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
        
        // Lưu danh sách sinh viên vào store
        if (data.students && Array.isArray(data.students)) {
          const studentList = data.students.map((student: any) => ({
            id: student.mssv || student.MSSV || '',
            name: student.hoTen || student.HoTen || 
                  (student.HoDem && student.Ten ? `${student.HoDem} ${student.Ten}` : '') || 
                  student.Ten || ''
          }))
          setStudentList(studentList)
          console.log('💾 Saved student list to store:', studentList)
        }
        
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
      <div className="max-w-6xl mx-auto px-4 py-8">
        <StepNavigation currentStep={2} />

        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-6 h-6" />
              Bước 2: Tải Lên Danh Sách Lớp
            </CardTitle>
            <CardDescription>Tải lên file Excel chứa danh sách sinh viên. File phải có định dạng .xlsx</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
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
                <AlertDescription className={uploadResult.success ? "text-green-800" : "text-red-800"}>
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
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Xem trước danh sách sinh viên:</h3>
                <div className="border rounded-lg overflow-hidden">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-16">STT</TableHead>
                        <TableHead>MSSV</TableHead>
                        <TableHead>Họ và Tên</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {students.slice(0, 5).map((student) => (
                        <TableRow key={student.stt}>
                          <TableCell>{student.stt}</TableCell>
                          <TableCell className="font-mono">{student.mssv}</TableCell>
                          <TableCell>{student.hoTen}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
                {students.length > 5 && (
                  <p className="text-sm text-gray-600 text-center">
                    Hiển thị 5 sinh viên đầu tiên. Tổng cộng: {students.length} sinh viên
                  </p>
                )}
              </div>
            )}

            <div className="flex justify-between">
              <Button variant="outline" onClick={handleBack}>
                Quay Lại
              </Button>
              <Button onClick={handleNext} disabled={!uploadResult?.success}>
                Tiếp Tục
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
