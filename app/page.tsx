import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle, Upload, Users, FileImage, BarChart3, Download } from "lucide-react"

export default function HomePage() {
  const features = [
    {
      icon: Upload,
      title: "Tải lên đáp án",
      description: "Hỗ trợ file Excel với nhiều mã đề",
    },
    {
      icon: Users,
      title: "Quản lý danh sách",
      description: "Import danh sách sinh viên từ Excel",
    },
    {
      icon: FileImage,
      title: "Xử lý ảnh bài làm",
      description: "Nhận dạng tự động MSSV và mã đề",
    },
    {
      icon: BarChart3,
      title: "Chấm điểm tự động",
      description: "Tính điểm chính xác theo đáp án",
    },
    {
      icon: CheckCircle,
      title: "Kiểm tra & chỉnh sửa",
      description: "Xem lại và sửa các lỗi nhận dạng",
    },
    {
      icon: Download,
      title: "Xuất kết quả",
      description: "Tải file Excel kết quả cuối cùng",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-0">
            <h1 className="text-lg sm:text-2xl font-bold text-gray-900 text-center sm:text-left">
              Hệ Thống Chấm Thi Trắc Nghiệm
            </h1>
            <Link href="/guide">
              <Button variant="outline" className="w-full sm:w-auto">Hướng dẫn</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-8 sm:py-16">
        <div className="text-center">
          <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold text-gray-900 mb-4 sm:mb-6 leading-tight">
            Hệ Thống Chấm Thi
            <span className="text-blue-600 block mt-2">Trắc Nghiệm Tự Động</span>
          </h2>
          <p className="text-base sm:text-xl text-gray-600 mb-6 sm:mb-8 max-w-3xl mx-auto px-2">
            Giải pháp hiện đại giúp giáo viên chấm thi trắc nghiệm một cách nhanh chóng, chính xác và tiện lợi. Chỉ cần
            5 bước đơn giản để có kết quả hoàn chỉnh.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center px-4">
            <Link href="/exam/step-1" className="w-full sm:w-auto">
              <Button size="lg" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3">
                Bắt Đầu Chấm Thi
              </Button>
            </Link>
            <Link href="/exam/step-1" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3 bg-transparent">
                Tạo Kỳ Thi Mới
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-8 sm:py-16">
        <div className="text-center mb-8 sm:mb-12">
          <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">Tính Năng Nổi Bật</h3>
          <p className="text-base sm:text-lg text-gray-600 px-2">Quy trình chấm thi được tối ưu hóa với công nghệ AI hiện đại</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3 sm:pb-6">
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-3 sm:mb-4">
                  <feature.icon className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
                </div>
                <CardTitle className="text-lg sm:text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <CardDescription className="text-sm sm:text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Process Overview */}
      <section className="bg-white py-8 sm:py-16">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
          <div className="text-center mb-8 sm:mb-12">
            <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">Quy Trình 5 Bước Đơn Giản</h3>
            <p className="text-base sm:text-lg text-gray-600 px-2">Từ tải lên đáp án đến xuất kết quả, mọi thứ đều được tự động hóa</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 sm:gap-4">
            {[
              { step: 1, title: "Đáp Án", desc: "Tải file Excel đáp án" },
              { step: 2, title: "Danh Sách", desc: "Import danh sách sinh viên" },
              { step: 3, title: "Bài Làm", desc: "Upload ảnh bài thi" },
              { step: 4, title: "Kiểm Tra", desc: "Xem và chỉnh sửa" },
              { step: 5, title: "Kết Quả", desc: "Xuất file Excel" },
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-lg sm:text-xl font-bold mx-auto mb-3 sm:mb-4">
                  {item.step}
                </div>
                <h4 className="font-semibold text-base sm:text-lg mb-2">{item.title}</h4>
                <p className="text-gray-600 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-6 sm:py-8">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 text-center">
          <p className="text-sm sm:text-base">&copy; 2024 Hệ Thống Chấm Thi Trắc Nghiệm Tự Động. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
