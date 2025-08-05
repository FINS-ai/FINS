import {
    BarChart3,
    Brain,
    LogOut,
    Menu,
    Settings,
    TrendingUp,
    User,
    Wallet,
    X
} from 'lucide-react';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Finanças', href: '/finances', icon: Wallet },
    { name: 'IA Insights', href: '/ai-insights', icon: Brain },
    { name: 'Relatórios', href: '/reports', icon: TrendingUp },
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">F</span>
              </div>
              <span className="text-xl font-bold text-gray-900">FINS</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  <Icon size={18} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <User size={16} className="text-primary-600" />
              </div>
              <span className="text-sm font-medium text-gray-700">
                {user?.full_name}
              </span>
            </div>
            
            <div className="relative">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
              >
                <Settings size={20} />
              </button>

              {isMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200">
                  <Link
                    to="/profile"
                    className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <User size={16} />
                    <span>Perfil</span>
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-2 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <LogOut size={16} />
                    <span>Sair</span>
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <Icon size={20} />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
              
              <div className="border-t border-gray-200 pt-4 mt-4">
                <div className="flex items-center space-x-2 px-3 py-2">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <User size={16} className="text-primary-600" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">
                    {user?.full_name}
                  </span>
                </div>
                
                <Link
                  to="/profile"
                  className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-primary-600 text-base font-medium"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <User size={20} />
                  <span>Perfil</span>
                </Link>
                
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 w-full px-3 py-2 text-gray-600 hover:text-primary-600 text-base font-medium"
                >
                  <LogOut size={20} />
                  <span>Sair</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header; 