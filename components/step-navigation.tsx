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
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between">
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
    </div>
  )
}
