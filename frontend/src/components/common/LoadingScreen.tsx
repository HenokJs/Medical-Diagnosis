/**
 * Fullscreen Loading Screen
 */

import LoadingSpinner from "./LoadingSpinner";

interface LoadingScreenProps {
  title?: string;
  subtitle?: string;
}

const LoadingScreen = ({
  title = "Processing...",
  subtitle,
}: LoadingScreenProps) => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="card p-8 max-w-md text-center">
        <LoadingSpinner size="lg" />
        <h2 className="text-lg font-semibold text-gray-900 mt-4">{title}</h2>
        {subtitle && <p className="text-sm text-gray-600 mt-2">{subtitle}</p>}
      </div>
    </div>
  );
};

export default LoadingScreen;
