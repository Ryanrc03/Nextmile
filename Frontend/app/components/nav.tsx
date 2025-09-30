import Link from "next/link";
import { metaData } from "../lib/config";

const navItems = {
  "/": { name: "HOME" },
  "/about": { name: "ABOUT" },
  "/education": { name: "EDUCATION" },
  "/experiences": { name: "EXPERIENCES" },
  "/skills": { name: "SKILLS" },
  "/contact": { name: "CONTACT ME" }
};

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/95 backdrop-blur-sm border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-white hover:text-[#00D9FF] transition-colors">
              Portfolio
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {Object.entries(navItems).map(([path, { name }]) => (
              <Link
                key={path}
                href={path}
                className="text-gray-300 hover:text-[#00D9FF] transition-all duration-300 font-medium text-sm relative group"
              >
                {name}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[#00D9FF] transition-all duration-300 group-hover:w-full"></span>
              </Link>
            ))}
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-gray-300 hover:text-[#00D9FF] transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
