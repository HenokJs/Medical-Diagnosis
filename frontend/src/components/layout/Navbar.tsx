/**
 * Modern Elegant Navbar
 * New Color Palette: Cream, Tan, Burgundy, Charcoal
 */

import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { 
  Activity, 
  FileText, 
  BarChart3, 
  Menu, 
  X,
  Stethoscope,
  BookOpen
} from "lucide-react";
import { ROUTES } from "@/constants";

const Navbar = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigation = [
    { name: "Diagnosis", href: ROUTES.DIAGNOSIS, icon: Activity },
    { name: "Results", href: ROUTES.RESULTS, icon: BarChart3 },
    { name: "Reports", href: ROUTES.REPORTS, icon: FileText },
    { name: "Disease Guide", href: "/disease-guide", icon: BookOpen },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-white border-b border-tan-200 shadow-soft sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link 
            to={ROUTES.DASHBOARD} 
            className="flex items-center space-x-3 group"
          >
            <div className="w-10 h-10 bg-gradient-elegant rounded-soft flex items-center justify-center shadow-soft group-hover:shadow-medium transition-all duration-300">
              <Stethoscope className="w-6 h-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-display font-bold text-burgundy">
                MediDiagnose
              </h1>
              <p className="text-xs text-tan-600 -mt-1">AI Clinical Support</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-soft text-sm font-medium
                    transition-all duration-200
                    ${active
                      ? "bg-burgundy text-white shadow-soft"
                      : "text-charcoal hover:bg-cream hover:text-burgundy"
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Link
              to={ROUTES.DIAGNOSIS}
              className="btn btn-primary flex items-center space-x-2"
            >
              <Activity className="w-4 h-4" />
              <span>New Diagnosis</span>
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-soft text-charcoal hover:bg-cream transition-colors"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-tan-200 bg-white">
          <div className="px-4 py-3 space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`
                    flex items-center space-x-3 px-4 py-3 rounded-soft text-sm font-medium
                    transition-all duration-200
                    ${active
                      ? "bg-burgundy text-white"
                      : "text-charcoal hover:bg-cream"
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
            
            <Link
              to={ROUTES.DIAGNOSIS}
              onClick={() => setMobileMenuOpen(false)}
              className="btn btn-primary w-full flex items-center justify-center space-x-2 mt-4"
            >
              <Activity className="w-4 h-4" />
              <span>New Diagnosis</span>
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
