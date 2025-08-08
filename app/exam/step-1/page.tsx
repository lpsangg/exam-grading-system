"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { FileText, CheckCircle, AlertCircle } from "lucide-react"
import { useExamStore } from "@/lib/store"
import { StepNavigation } from "@/components/step-navigation"
import { FileUpload } from "@/components/file-upload"
import { toast } from "sonner"

export default function Step1Page() {
  const router = useRouter()
  const { setAnswerFile, answerFile, setExamCodes } = useExamStore()
  const [isUploading, setIsUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<{
    success: boolean
    message: string
    examCodes?: string[]
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
      
      console.log('Sending request to:', 'http://localhost:5000/api/upload_answer_key');
      console.log('File:', file.name, 'Size:', file.size);
      
      const res = await fetch('http://localhost:5000/api/upload_answer_key', {
        method: 'POST',
        body: formData,
      });
      
      console.log('Response status:', res.status);
      console.log('Response ok:', res.ok);
      
      const data = await res.json();
      console.log('Response data:', data);
      
      if (res.ok) {
        setAnswerFile(file)
        // Lưu danh sách mã đề vào store
        if (data.examCodes && Array.isArray(data.examCodes)) {
          setExamCodes(data.examCodes)
        }
        setUploadResult({
          success: true,
          message: data.message,
          examCodes: data.examCodes || [],
        })
        toast.success("Tải lên đáp án thành công!")
      } else {
        console.log('API returned error:', data);
        setUploadResult({ success: false, message: data.error || 'Lỗi không xác định' })
        toast.error(data.error || "Có lỗi xảy ra khi tải file")
      }
    } catch (error) {
      console.error('Network or other error:', error);
      setUploadResult({ 
        success: false, 
        message: `Lỗi kết nối: ${error instanceof Error ? error.message : 'Không thể kết nối đến server'}` 
      })
      toast.error("Không thể kết nối đến server. Vui lòng kiểm tra backend có đang chạy không.")
    } finally {
      setIsUploading(false)
    }
  }

  const handleNext = () => {
    router.push("/exam/step-2")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-3 sm:px-6 py-4 sm:py-8">
        <StepNavigation currentStep={1} />

        <Card className="mt-4 sm:mt-8">
          <CardHeader className="pb-4 sm:pb-6">
            <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
              <FileText className="w-5 h-5 sm:w-6 sm:h-6" />
              Bước 1: Tải Lên Đáp Án
            </CardTitle>
            <CardDescription className="text-sm sm:text-base">
              Tải lên file Excel chứa đáp án cho các mã đề thi. File phải có định dạng .xlsx
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4 sm:space-y-6">
            <FileUpload
              onFileSelect={handleFileUpload}
              accept=".xlsx"
              disabled={isUploading}
              title="Kéo thả file đáp án vào đây hoặc click để chọn"
              description="Chỉ chấp nhận file Excel (.xlsx)"
            />

            {isUploading && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-sm">Đang xử lý file...</span>
                </div>
                <Progress value={75} className="w-full" />
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
                  {uploadResult.examCodes && (
                    <div className="mt-2">
                      <strong>Mã đề được tìm thấy:</strong> {uploadResult.examCodes.join(", ")}
                    </div>
                  )}
                </AlertDescription>
              </Alert>
            )}

            <div className="flex flex-col sm:flex-row justify-between gap-3 sm:gap-0">
              <Button variant="outline" onClick={() => router.push("/")} className="w-full sm:w-auto">
                Về Trang Chủ
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
