import type React from "react"
import type { Metadata, Viewport } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Toaster } from "sonner"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Hệ Thống Chấm Thi Trắc Nghiệm Tự Động",
  description: "Giải pháp chấm thi trắc nghiệm tự động với AI",
  generator: 'PhuocSang'
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

// Component để tránh hydration issues
function ToasterWrapper() {
  return <Toaster position="top-right" />
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
        <ToasterWrapper />
      </body>
    </html>
  )
}
