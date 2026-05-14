/**
 * Sidebar Navigation
 * Desktop-only quick navigation
 */

import { Link, useLocation } from "react-router-dom";
import { Activity, Stethoscope, FileText, ActivitySquare } from "lucide-react";
import { ROUTES } from "@/constants";

const Sidebar = () => {
  const location = useLocation();

  const navigation = [
    { name: "Dashboard", href: ROUTES.HOME, icon: Activity },
    { name: "Diagnosis", href: ROUTES.DIAGNOSIS, icon: Stethoscope },
    { name: "Reports", href: ROUTES.REPORTS, icon: FileText },
    { name: "System Status", href: ROUTES.STATUS, icon: ActivitySquare },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside className="hidden lg:block w-64 bg-white border-r border-gray-200">
      <div className="p-6">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-4">
          Navigation
        </h3>
        <nav className="space-y-2">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive(item.href)
                  ? "bg-primary-50 text-primary-700"
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-50"
              }`}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.name}</span>
            </Link>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
