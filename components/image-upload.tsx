"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { FileImage, X } from "lucide-react"
import { toast } from "sonner"
import Image from "next/image"

interface ImageUploadProps {
  onImagesSelected: (images: File[]) => void
  selectedImages: File[]
  onRemoveImage: (index: number) => void
}

export function ImageUpload({ onImagesSelected, selectedImages, onRemoveImage }: ImageUploadProps) {
  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    const imageFiles = files.filter((file) => file.type.startsWith("image/"))

    if (imageFiles.length !== files.length) {
      toast.error("Chỉ chấp nhận file ảnh (JPG, PNG, etc.)")
    }

    onImagesSelected(imageFiles)
  }

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    const files = Array.from(event.dataTransfer.files)
    const imageFiles = files.filter((file) => file.type.startsWith("image/"))

    if (imageFiles.length !== files.length) {
      toast.error("Chỉ chấp nhận file ảnh (JPG, PNG, etc.)")
    }

    onImagesSelected(imageFiles)
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  return (
    <div className="space-y-6">
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <FileImage className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold mb-2">Kéo thả ảnh bài làm vào đây</h3>
        <p className="text-gray-600 mb-4">hoặc</p>
        <label htmlFor="image-upload">
          <Button variant="outline" className="cursor-pointer bg-transparent">
            Chọn Ảnh
          </Button>
        </label>
        <input
          id="image-upload"
          type="file"
          multiple
          accept="image/*"
          className="hidden"
          onChange={handleImageSelect}
        />
        <p className="text-sm text-gray-500 mt-2">Hỗ trợ JPG, PNG, GIF. Có thể chọn nhiều file cùng lúc.</p>
      </div>

      {selectedImages.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Ảnh đã chọn ({selectedImages.length} file):</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {selectedImages.map((image, index) => (
              <div key={index} className="relative group">
                <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                  <Image
                    src={URL.createObjectURL(image) || "/placeholder.svg"}
                    alt={image.name}
                    width={200}
                    height={200}
                    className="w-full h-full object-cover"
                  />
                </div>
                <button
                  onClick={() => onRemoveImage(index)}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="w-4 h-4" />
                </button>
                <p className="text-xs text-gray-600 mt-1 truncate">{image.name}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
} 