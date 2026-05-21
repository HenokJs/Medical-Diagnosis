/**
 * Toast notifications provider
 */

import { createContext, useContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import {
  CheckCircle,
  XCircle,
  Info,
  AlertTriangle,
  X,
} from "lucide-react";

export type ToastType = "success" | "error" | "info" | "warning";

interface ToastItem {
  id: string;
  type: ToastType;
  title?: string;
  message: string;
  durationMs?: number;
}

interface ToastContextValue {
  notify: (type: ToastType, message: string, title?: string, durationMs?: number) => void;
  success: (message: string, title?: string) => void;
  error: (message: string, title?: string) => void;
  info: (message: string, title?: string) => void;
  warning: (message: string, title?: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

const iconByType: Record<ToastType, JSX.Element> = {
  success: <CheckCircle className="w-5 h-5 text-emerald-600" />,
  error: <XCircle className="w-5 h-5 text-red-600" />,
  info: <Info className="w-5 h-5 text-blue-600" />,
  warning: <AlertTriangle className="w-5 h-5 text-amber-600" />,
};

const borderByType: Record<ToastType, string> = {
  success: "border-emerald-200 bg-emerald-50",
  error: "border-red-200 bg-red-50",
  info: "border-blue-200 bg-blue-50",
  warning: "border-amber-200 bg-amber-50",
};

export const ToastProvider = ({ children }: { children: ReactNode }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = (id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  };

  const notify = (
    type: ToastType,
    message: string,
    title?: string,
    durationMs: number = 3500
  ) => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const toast: ToastItem = { id, type, message, title, durationMs };
    setToasts((current) => [...current, toast]);

    if (durationMs > 0) {
      window.setTimeout(() => removeToast(id), durationMs);
    }
  };

  const value = useMemo<ToastContextValue>(
    () => ({
      notify,
      success: (message, title) => notify("success", message, title),
      error: (message, title) => notify("error", message, title),
      info: (message, title) => notify("info", message, title),
      warning: (message, title) => notify("warning", message, title),
    }),
    [notify]
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed top-4 right-4 z-[100] space-y-3">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`w-[320px] border rounded-lg shadow-lg p-4 ${borderByType[toast.type]}`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-start gap-3">
                {iconByType[toast.type]}
                <div>
                  <p className="text-sm font-semibold text-gray-900">
                    {toast.title || "Notification"}
                  </p>
                  <p className="text-sm text-gray-700 mt-1">
                    {toast.message}
                  </p>
                </div>
              </div>
              <button
                onClick={() => removeToast(toast.id)}
                className="text-gray-500 hover:text-gray-700"
                aria-label="Close notification"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
};
