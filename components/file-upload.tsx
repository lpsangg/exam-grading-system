"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Upload, FileText } from "lucide-react"

interface FileUploadProps {
  onFileSelect: (file: File) => void
  accept: string
  disabled?: boolean
  title: string
  description: string
}

export function FileUpload({ onFileSelect, accept, disabled, title, description }: FileUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false)

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    setIsDragOver(false)

    if (disabled) return

    const files = Array.from(event.dataTransfer.files)
    if (files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
    if (!disabled) {
      setIsDragOver(true)
    }
  }

  const handleDragLeave = (event: React.DragEvent) => {
    event.preventDefault()
    setIsDragOver(false)
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-4 sm:p-8 text-center transition-colors ${
        isDragOver ? "border-blue-400 bg-blue-50" : "border-gray-300 hover:border-gray-400"
      } ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <FileText className="w-10 h-10 sm:w-12 sm:h-12 text-gray-400 mx-auto mb-3 sm:mb-4" />
      <h3 className="text-base sm:text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm sm:text-base text-gray-600 mb-3 sm:mb-4 px-2">{description}</p>

      <div>
        <input
          id="file-upload"
          type="file"
          accept={accept}
          className="hidden"
          onChange={handleFileSelect}
          disabled={disabled}
        />
        <label 
          htmlFor="file-upload" 
          className={`inline-block w-full sm:w-auto px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <Upload className="w-4 h-4 mr-2 inline" />
          Chọn File
        </label>
      </div>
    </div>
  )
}
