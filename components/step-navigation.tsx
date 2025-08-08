import { CheckCircle } from "lucide-react"

interface StepNavigationProps {
  currentStep: number
}

export function StepNavigation({ currentStep }: StepNavigationProps) {
  const steps = [
    { number: 1, title: "Đáp Án" },
    { number: 2, title: "Danh Sách" },
    { number: 3, title: "Bài Làm" },
    { number: 4, title: "Kết Quả" },
    { number: 5, title: "Xuất File" },
  ]

  return (
    <div className="bg-white rounded-lg shadow-sm p-3 sm:p-6">
      {/* Desktop Navigation */}
      <div className="hidden sm:flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.number} className="flex items-center">
            <div className="flex flex-col items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${
                  step.number < currentStep
                    ? "bg-green-500 border-green-500 text-white"
                    : step.number === currentStep
                      ? "bg-blue-500 border-blue-500 text-white"
                      : "bg-gray-100 border-gray-300 text-gray-400"
                }`}
              >
                {step.number < currentStep ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  <span className="font-semibold">{step.number}</span>
                )}
              </div>
              <span
                className={`text-sm mt-2 font-medium ${step.number <= currentStep ? "text-gray-900" : "text-gray-400"}`}
              >
                {step.title}
              </span>
            </div>

            {index < steps.length - 1 && (
              <div className={`w-16 h-0.5 mx-4 ${step.number < currentStep ? "bg-green-500" : "bg-gray-300"}`} />
            )}
          </div>
        ))}
      </div>

      {/* Mobile Navigation */}
      <div className="flex sm:hidden items-center justify-center">
        <div className="text-center">
          <div
            className={`w-12 h-12 rounded-full flex items-center justify-center border-2 mx-auto ${
              currentStep > 1 
                ? "bg-green-500 border-green-500 text-white"
                : "bg-blue-500 border-blue-500 text-white"
            }`}
          >
            {currentStep > 1 && currentStep <= steps.length ? (
              <CheckCircle className="w-6 h-6" />
            ) : (
              <span className="font-semibold text-lg">{currentStep}</span>
            )}
          </div>
          <div className="mt-2">
            <span className="text-blue-600 font-semibold text-base">
              Bước {currentStep}
            </span>
            <div className="text-gray-600 text-sm">
              {steps[currentStep - 1]?.title}
            </div>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {currentStep} / {steps.length}
          </div>
        </div>
      </div>
    </div>
  )
}
