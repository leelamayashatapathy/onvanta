import type { InputHTMLAttributes } from "react";

interface RadioOption {
  value: string;
  label: string;
  helper?: string;
}

interface RadioGroupProps extends InputHTMLAttributes<HTMLInputElement> {
  name: string;
  options: RadioOption[];
}

export function RadioGroup({ name, options, ...props }: RadioGroupProps) {
  return (
    <div className="space-y-3">
      {options.map((option) => (
        <label key={option.value} className="flex items-start gap-3 text-sm text-slate-700">
          <input
            type="radio"
            name={name}
            value={option.value}
            className="mt-1 h-4 w-4 border-slate-300 text-blue-600 focus:ring-blue-500"
            {...props}
          />
          <div>
            <p className="font-medium text-slate-800">{option.label}</p>
            {option.helper ? <p className="text-xs text-slate-500">{option.helper}</p> : null}
          </div>
        </label>
      ))}
    </div>
  );
}
