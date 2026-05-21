/**
 * PDF Report Preview Modal
 */

import { X, Download, Printer } from "lucide-react";
import LoadingSpinner from "@/components/common/LoadingSpinner";

interface ReportPdfModalProps {
  open: boolean;
  title?: string;
  pdfUrl?: string | null;
  loading?: boolean;
  onClose: () => void;
  onDownload: () => void;
  onPrint: () => void;
}

const ReportPdfModal = ({
  open,
  title = "Report Preview",
  pdfUrl,
  loading = false,
  onClose,
  onDownload,
  onPrint,
}: ReportPdfModalProps) => {
  if (!open) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="relative w-[95%] max-w-5xl h-[85vh] bg-white rounded-2xl shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
            <p className="text-sm text-gray-500">PDF preview and actions</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onPrint}
              className="btn btn-outline flex items-center disabled:opacity-60"
              disabled={loading || !pdfUrl}
            >
              <Printer className="w-4 h-4 mr-2" />
              Print
            </button>
            <button
              onClick={onDownload}
              className="btn btn-secondary flex items-center disabled:opacity-60"
              disabled={loading || !pdfUrl}
            >
              <Download className="w-4 h-4 mr-2" />
              Download
            </button>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
              aria-label="Close report preview"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="h-[calc(85vh-72px)]">
          {loading ? (
            <div className="h-full flex items-center justify-center">
              <LoadingSpinner text="Loading report preview..." />
            </div>
          ) : pdfUrl ? (
            <iframe src={pdfUrl} title="Report PDF" className="w-full h-full" />
          ) : (
            <div className="h-full flex items-center justify-center">
              <p className="text-sm text-gray-500">No report available</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportPdfModal;
