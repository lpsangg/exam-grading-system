"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { FileImage } from "lucide-react"

export default function TestButton() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    setSelectedFiles(files)
    console.log("Files selected:", files)
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test Button Click</h1>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <FileImage className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold mb-2">Test Upload</h3>
        <p className="text-gray-600 mb-4">Click button below:</p>
        
        <Button 
          variant="outline" 
          className="bg-transparent cursor-pointer"
          onClick={() => document.getElementById('test-file-input')?.click()}
        >
          Chọn Ảnh
        </Button>
        
        <input
          id="test-file-input"
          type="file"
          multiple
          accept="image/*"
          className="hidden"
          onChange={handleFileSelect}
        />
        
        <p className="text-sm text-gray-500 mt-2">
          Selected files: {selectedFiles.length}
        </p>
        
        {selectedFiles.length > 0 && (
          <div className="mt-4">
            <h4>Selected files:</h4>
            <ul className="text-sm">
              {selectedFiles.map((file, index) => (
                <li key={index}>{file.name}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
} 