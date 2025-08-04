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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Hệ Thống Chấm Thi Trắc Nghiệm</h1>
            <Link href="/guide">
              <Button variant="outline">Hướng dẫn</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Hệ Thống Chấm Thi
            <span className="text-blue-600 block">Trắc Nghiệm Tự Động</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Giải pháp hiện đại giúp giáo viên chấm thi trắc nghiệm một cách nhanh chóng, chính xác và tiện lợi. Chỉ cần
            5 bước đơn giản để có kết quả hoàn chỉnh.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/exam/step-1">
              <Button size="lg" className="text-lg px-8 py-3">
                Bắt Đầu Chấm Thi
              </Button>
            </Link>
            <Link href="/exam/step-1">
              <Button size="lg" variant="outline" className="text-lg px-8 py-3 bg-transparent">
                Tạo Kỳ Thi Mới
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">Tính Năng Nổi Bật</h3>
          <p className="text-lg text-gray-600">Quy trình chấm thi được tối ưu hóa với công nghệ AI hiện đại</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Process Overview */}
      <section className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Quy Trình 5 Bước Đơn Giản</h3>
            <p className="text-lg text-gray-600">Từ tải lên đáp án đến xuất kết quả, mọi thứ đều được tự động hóa</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { step: 1, title: "Đáp Án", desc: "Tải file Excel đáp án" },
              { step: 2, title: "Danh Sách", desc: "Import danh sách sinh viên" },
              { step: 3, title: "Bài Làm", desc: "Upload ảnh bài thi" },
              { step: 4, title: "Kiểm Tra", desc: "Xem và chỉnh sửa" },
              { step: 5, title: "Kết Quả", desc: "Xuất file Excel" },
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h4 className="font-semibold text-lg mb-2">{item.title}</h4>
                <p className="text-gray-600 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 Hệ Thống Chấm Thi Trắc Nghiệm Tự Động. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
