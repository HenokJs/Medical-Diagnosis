import { APP_VERSION } from '@/constants';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      {/* Medical Disclaimer */}
      <div className="bg-blue-50 border-b border-blue-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        </div>
      </div>

      {/* Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="text-center md:text-left">
            <p className="text-sm text-gray-600">
              © {new Date().getFullYear()} Medical Diagnosis System
            </p>
            <p className="text-xs text-gray-500 mt-1">
              AI-Powered Clinical Decision Support • Version {APP_VERSION}
            </p>
          </div>

          <div className="flex items-center space-x-6 text-sm text-gray-600">
            <a href="#" className="hover:text-primary-600 transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-primary-600 transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-primary-600 transition-colors">
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
