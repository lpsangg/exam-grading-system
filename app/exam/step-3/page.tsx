"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { FileImage, X, Play, CheckCircle, Building, ZoomIn } from "lucide-react"
import { useExamStore } from "@/lib/store"
import { StepNavigation } from "@/components/step-navigation"
import { toast } from "sonner"
import Image from "next/image"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"


interface ProcessingStatus {
  status: "idle" | "processing" | "completed" | "error"
  progress: {
    completed: number
    total: number
  }
  jobId?: string
  message?: string
}

export default function Step3Page() {
  const router = useRouter()
  const { setExamImages, examImages, selectedRoom, setSelectedRoom, calculatedRooms, studentCount, answerFile, studentFile, setExamResults, setStudentList } = useExamStore()
  const [selectedImages, setSelectedImages] = useState<File[]>([])
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus>({
    status: "idle",
    progress: { completed: 0, total: 0 },
  })

  // Modal state
  const [selectedImageIndex, setSelectedImageIndex] = useState<number | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  // Danh sách phòng thi được tính toán
  const [loadingRooms, setLoadingRooms] = useState(false)

  // Sử dụng phòng thi được tính toán từ step-2
  useEffect(() => {
    if (calculatedRooms.length > 0) {
      setLoadingRooms(false)
    }
  }, [calculatedRooms])

  const removeImage = (index: number) => {
    setSelectedImages((prev) => prev.filter((_, i) => i !== index))
  }

  const openImageModal = (index: number) => {
    setSelectedImageIndex(index)
    setIsModalOpen(true)
  }

  const closeImageModal = () => {
    setIsModalOpen(false)
    setSelectedImageIndex(null)
  }

  const startProcessing = async () => {
    if (!selectedRoom) {
      toast.error("Vui lòng chọn phòng thi")
      return
    }
    
    if (selectedImages.length === 0) {
      toast.error("Vui lòng chọn ít nhất một ảnh bài làm")
      return
    }

    if (!answerFile) {
      toast.error("Vui lòng quay lại bước 1 để tải đáp án")
      return
    }

    if (!studentFile) {
      toast.error("Vui lòng quay lại bước 2 để tải danh sách sinh viên")
      return
    }

    setProcessingStatus({
      status: "processing",
      progress: { completed: 0, total: selectedImages.length },
      jobId: "job_12345",
    })

    try {
      console.log('🚀 Bắt đầu xử lý...')
      console.log('📁 Files từ store:', { answerFile: answerFile?.name, studentFile: studentFile?.name })
      
      // 1. Upload ảnh lên backend
      console.log('📤 Uploading images...')
      const formData = new FormData();
      selectedImages.forEach((file) => formData.append('images', file));
      const uploadRes = await fetch('http://localhost:5000/api/upload_exam_images', {
        method: 'POST',
        body: formData,
      });
      const uploadData = await uploadRes.json();
      console.log('📤 Upload response:', uploadData)
      if (!uploadRes.ok) throw new Error(uploadData.error || 'Lỗi upload ảnh');
      const imageFilenames = uploadData.files;

      // 2. Gọi API xử lý ảnh
      console.log('⚙️ Processing images...')
      const answerKeyFilename = answerFile?.name || ''
      const studentListFilename = studentFile?.name || ''
      const room = selectedRoom
      
      const processPayload = {
        answer_key_filename: answerKeyFilename,
        student_list_filename: studentListFilename,
        image_filenames: imageFilenames,
        room,
      }
      console.log('📦 Process payload:', processPayload)
      
      const processRes = await fetch('http://localhost:5000/api/process_images', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(processPayload),
      });
      const processData = await processRes.json();
      console.log('⚙️ Process response:', processData)
      if (!processRes.ok) throw new Error(processData.error || 'Lỗi xử lý ảnh');

      setProcessingStatus({
        status: "completed",
        progress: { completed: selectedImages.length, total: selectedImages.length },
        jobId: "job_12345",
      })
      setExamImages(selectedImages)
      
      // Transform backend data to frontend format
      const transformedResults = processData.results.map((student: any) => ({
        id: student.id || 'N/A',
        imageName: student.image || 'unknown',
        recognizedStudentId: student.id || 'N/A',
        recognizedExamCode: student.testVariant || 'N/A',
        score: student.score || 0,
        status: student.has_issue ? "warning" : (student.score > 0 ? "success" : "error"),
        imageUrl: `http://localhost:5000/api/images/${student.image}` || "/placeholder.svg",
        name: student.name || 'N/A',
        indexStudent: student.index_student || 'N/A',
        answers: student.answers || [],
        numQuestions: student.num_questions || 0
      }))
      
      console.log('🔄 Transformed results:', transformedResults)
      setExamResults(transformedResults) // Lưu kết quả đã transform vào store
      
      // Lưu danh sách sinh viên từ kết quả (loại bỏ trùng lặp)
      const uniqueStudents = transformedResults
        .filter((student: any) => student.id && student.id !== 'N/A')
        .reduce((acc: any[], student: any) => {
          const exists = acc.find(s => s.id === student.id)
          if (!exists) {
            acc.push({
              id: student.id,
              name: student.name || 'N/A'
            })
          }
          return acc
        }, [])
      
      setStudentList(uniqueStudents)
      console.log('👥 Saved student list:', uniqueStudents)
      
      toast.success("Xử lý hoàn tất!")

      setTimeout(() => {
        router.push("/exam/step-4")
      }, 2000)
    } catch (error: any) {
      setProcessingStatus((prev) => ({ ...prev, status: "error", message: error.message }))
      toast.error(error.message || "Có lỗi xảy ra khi xử lý ảnh")
    }
  }

  const handleBack = () => {
    router.push("/exam/step-2")
  }

  const progressPercentage =
    processingStatus.progress.total > 0
      ? (processingStatus.progress.completed / processingStatus.progress.total) * 100
      : 0

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <StepNavigation currentStep={3} />

        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileImage className="w-6 h-6" />
              Bước 3: Tải Lên & Xử Lý Bài Làm
            </CardTitle>
            <CardDescription>Tải lên ảnh bài làm của sinh viên và kích hoạt quá trình xử lý tự động</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {processingStatus.status === "idle" && (
              <>
                {/* Chọn phòng thi */}
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <Building className="w-5 h-5 text-gray-600" />
                    <h3 className="text-lg font-semibold">Chọn phòng thi</h3>
                  </div>
                  {loadingRooms ? (
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span className="text-sm text-gray-600">Đang tải danh sách phòng thi...</span>
                    </div>
                  ) : calculatedRooms.length > 0 ? (
                    <>
                      <div className="space-y-3">
                        <p className="text-sm text-gray-600">
                          📊 Tổng số sinh viên: <strong>{studentCount}</strong> → Tự động chia thành <strong>{calculatedRooms.length}</strong> phòng thi
                        </p>
                        <Select value={selectedRoom} onValueChange={setSelectedRoom}>
                          <SelectTrigger className="w-full max-w-md">
                            <SelectValue placeholder="Chọn phòng thi..." />
                          </SelectTrigger>
                          <SelectContent>
                            {calculatedRooms.map((room) => (
                              <SelectItem key={room.id} value={room.id}>
                                {room.name} ({room.student_count} sinh viên)
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        {selectedRoom && (
                          <p className="text-sm text-green-600">
                            ✅ Đã chọn: {calculatedRooms.find(r => r.id === selectedRoom)?.name} 
                            ({calculatedRooms.find(r => r.id === selectedRoom)?.student_count} sinh viên)
                          </p>
                        )}
                      </div>
                    </>
                  ) : (
                    <div className="text-sm text-orange-600">
                      ⚠️ Vui lòng quay lại bước 2 để tải danh sách sinh viên trước
                    </div>
                  )}
                </div>

                <div className="border-t pt-6">
                  <div className="flex items-center gap-2 mb-4">
                    <FileImage className="w-5 h-5 text-gray-600" />
                    <h3 className="text-lg font-semibold">Tải lên ảnh bài làm</h3>
                  </div>
                  
                  {/* Upload ảnh trực tiếp */}
                  <div className="space-y-6">
                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors"
                      onDrop={(e) => {
                        e.preventDefault()
                        const files = Array.from(e.dataTransfer.files)
                        const imageFiles = files.filter((file) => file.type.startsWith("image/"))
                        if (imageFiles.length !== files.length) {
                          toast.error("Chỉ chấp nhận file ảnh (JPG, PNG, etc.)")
                        }
                        setSelectedImages((prev) => [...prev, ...imageFiles])
                      }}
                      onDragOver={(e) => e.preventDefault()}
                >
                  <FileImage className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Kéo thả ảnh bài làm vào đây</h3>
                  <p className="text-gray-600 mb-4">hoặc</p>
                      <Button 
                        variant="outline" 
                        className="bg-transparent cursor-pointer"
                        onClick={() => document.getElementById('image-upload')?.click()}
                      >
                      Chọn Ảnh
                    </Button>
                  <input
                    id="image-upload"
                    type="file"
                    multiple
                    accept="image/*"
                    className="hidden"
                        onChange={(e) => {
                          const files = Array.from(e.target.files || [])
                          const imageFiles = files.filter((file) => file.type.startsWith("image/"))
                          if (imageFiles.length !== files.length) {
                            toast.error("Chỉ chấp nhận file ảnh (JPG, PNG, etc.)")
                          }
                          setSelectedImages((prev) => [...prev, ...imageFiles])
                        }}
                  />
                  <p className="text-sm text-gray-500 mt-2">Hỗ trợ JPG, PNG, GIF. Có thể chọn nhiều file cùng lúc.</p>
                </div>

                {selectedImages.length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Ảnh đã chọn ({selectedImages.length} file):</h3>
                        <div className="border-2 border-gray-200 rounded-lg p-4 max-h-80 overflow-y-auto">
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                      {selectedImages.map((image, index) => (
                        <div key={index} className="relative group">
                                <div 
                                  className="aspect-square bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
                                  onClick={() => openImageModal(index)}
                                >
                            <Image
                              src={URL.createObjectURL(image) || "/placeholder.svg"}
                              alt={image.name}
                              width={200}
                              height={200}
                              className="w-full h-full object-cover"
                            />
                                  <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all flex items-center justify-center">
                                    <ZoomIn className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                                  </div>
                          </div>
                          <button
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    removeImage(index)
                                  }}
                                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity z-10"
                          >
                            <X className="w-4 h-4" />
                          </button>
                          <p className="text-xs text-gray-600 mt-1 truncate">{image.name}</p>
                        </div>
                      ))}
                          </div>
                    </div>
                  </div>
                )}
                  </div>
                </div>
              </>
            )}

            {processingStatus.status === "processing" && (
              <div className="space-y-4">
                <Alert className="border-blue-200 bg-blue-50">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <AlertDescription className="text-blue-800">
                    <strong>Đang xử lý...</strong> Hệ thống đang nhận dạng MSSV và mã đề từ {selectedImages.length} ảnh
                    bài làm.
                  </AlertDescription>
                </Alert>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Tiến độ xử lý</span>
                    <span>
                      {processingStatus.progress.completed}/{processingStatus.progress.total} ảnh
                    </span>
                  </div>
                  <Progress value={progressPercentage} className="w-full" />
                </div>
              </div>
            )}

            {processingStatus.status === "completed" && (
              <Alert className="border-green-200 bg-green-50">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">
                  <strong>Hoàn tất!</strong> Đã xử lý thành công {selectedImages.length} ảnh bài làm. Đang chuyển đến
                  bước kiểm tra kết quả...
                </AlertDescription>
              </Alert>
            )}

            <div className="flex justify-between">
              <Button variant="outline" onClick={handleBack} disabled={processingStatus.status === "processing"}>
                Quay Lại
              </Button>

              {processingStatus.status === "idle" && (
                <Button
                  onClick={startProcessing}
                  disabled={selectedImages.length === 0 || !selectedRoom}
                  className="flex items-center gap-2"
                >
                  <Play className="w-4 h-4" />
                  Xử Lý & Chấm Điểm
                </Button>
              )}

              {processingStatus.status === "completed" && (
                <Button onClick={() => router.push("/exam/step-4")}>Xem Kết Quả</Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Image Modal */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <FileImage className="w-5 h-5" />
              Xem ảnh chi tiết
            </DialogTitle>
          </DialogHeader>
          <div className="flex items-center justify-center p-4">
            {selectedImageIndex !== null && selectedImages[selectedImageIndex] && (
              <div className="relative">
                <Image
                  src={URL.createObjectURL(selectedImages[selectedImageIndex])}
                  alt={selectedImages[selectedImageIndex].name}
                  width={800}
                  height={600}
                  className="max-w-full max-h-[70vh] object-contain rounded-lg"
                />
                <div className="mt-4 text-center">
                  <p className="text-sm text-gray-600">
                    {selectedImages[selectedImageIndex].name} 
                    ({(selectedImages[selectedImageIndex].size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
