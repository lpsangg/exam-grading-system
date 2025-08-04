import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, FileText, Users, FileImage, BarChart3, Download } from "lucide-react"

export default function GuidePage() {
  const steps = [
    {
      icon: FileText,
      title: "Bước 1: Tải lên đáp án",
      description: "Chuẩn bị file Excel chứa đáp án cho các mã đề thi",
      details: [
        "File phải có định dạng .xlsx",
        "Mỗi sheet tương ứng với một mã đề",
        "Cột A: Số câu hỏi, Cột B: Đáp án đúng (A, B, C, D)",
      ],
    },
    {
      icon: Users,
      title: "Bước 2: Tải lên danh sách sinh viên",
      description: "Import danh sách lớp từ file Excel",
      details: [
        "File Excel với các cột: STT, MSSV, Họ và Tên",
        "MSSV phải chính xác để nhận dạng được",
        "Hệ thống sẽ hiển thị preview để kiểm tra",
      ],
    },
    {
      icon: FileImage,
      title: "Bước 3: Tải lên ảnh bài làm",
      description: "Upload ảnh bài thi và kích hoạt xử lý tự động",
      details: [
        "Hỗ trợ nhiều định dạng: JPG, PNG, GIF",
        "Có thể chọn nhiều file cùng lúc",
        "Hệ thống sẽ tự động nhận dạng MSSV và mã đề",
      ],
    },
    {
      icon: BarChart3,
      title: "Bước 4: Kiểm tra và chỉnh sửa",
      description: "Xem lại kết quả và sửa các lỗi nhận dạng",
      details: [
        "Kiểm tra các trường hợp MSSV không khớp",
        "Chỉnh sửa mã đề nếu nhận dạng sai",
        "Xem ảnh gốc để đối chiếu",
      ],
    },
    {
      icon: Download,
      title: "Bước 5: Xuất kết quả",
      description: "Tải xuống file Excel kết quả cuối cùng",
      details: [
        "File chứa đầy đủ thông tin: MSSV, Họ tên, Điểm",
        "Có thống kê tổng quan về kết quả thi",
        "Định dạng Excel tiện lợi cho việc lưu trữ",
      ],
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <Link href="/">
            <Button variant="outline" className="mb-4 bg-transparent">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Về Trang Chủ
            </Button>
          </Link>

          <h1 className="text-3xl font-bold text-gray-900 mb-4">Hướng Dẫn Sử Dụng Hệ Thống</h1>
          <p className="text-lg text-gray-600">Hướng dẫn chi tiết cách sử dụng hệ thống chấm thi trắc nghiệm tự động</p>
        </div>

        <div className="space-y-6">
          {steps.map((step, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <step.icon className="w-5 h-5 text-blue-600" />
                  </div>
                  {step.title}
                </CardTitle>
                <CardDescription className="text-base">{step.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {step.details.map((detail, detailIndex) => (
                    <li key={detailIndex} className="flex items-start gap-2">
                      <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-gray-700">{detail}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="mt-8 bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle className="text-blue-900">Lưu Ý Quan Trọng</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-blue-800">
            <p>• Đảm bảo ảnh bài làm có chất lượng tốt, không bị mờ hoặc nghiêng</p>
            <p>• MSSV và mã đề phải được viết rõ ràng trên bài thi để hệ thống nhận dạng chính xác</p>
            <p>• Kiểm tra kỹ file đáp án và danh sách sinh viên trước khi tải lên</p>
            <p>• Luôn xem lại kết quả ở bước 4 trước khi xuất file cuối cùng</p>
          </CardContent>
        </Card>

        <div className="mt-8 text-center">
          <Link href="/exam/step-1">
            <Button size="lg" className="px-8">
              Bắt Đầu Sử Dụng Hệ Thống
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
