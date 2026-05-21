/**
 * File download utilities
 */

export const getFilenameFromDisposition = (
  contentDisposition?: string,
): string | undefined => {
  if (!contentDisposition) {
    return undefined;
  }

  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1]);
    } catch {
      return utf8Match[1];
    }
  }

  const fallbackMatch = contentDisposition.match(/filename="?([^";]+)"?/i);
  return fallbackMatch?.[1];
};

export const downloadBlob = (
  blob: Blob,
  filename: string,
  mimeType?: string,
) => {
  const safeBlob = new Blob([blob], {
    type: mimeType || blob.type || "application/octet-stream",
  });
  const url = URL.createObjectURL(safeBlob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
};

export const createBlobUrl = (blob: Blob): string => {
  return URL.createObjectURL(blob);
};

export const revokeBlobUrl = (url?: string | null) => {
  if (url) {
    URL.revokeObjectURL(url);
  }
};
