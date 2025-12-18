import React from 'react';
import { BellIcon } from '../../icons';
import AuthSection from './AuthSection';

const Navbar = ({ auth, togglePanel }) => (
  <header className="fixed top-0 left-0 right-0 bg-app-dark border-b border-app-hover z-30">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center h-16">
        <div className="flex items-center">
          <h1 className="text-xl font-semibold text-white">My App</h1>
        </div>
        <div className="flex items-center space-x-4">
          <AuthSection 
            isLoggedIn={auth.isLoggedIn}
            handleLogout={auth.handleLogout}
            showAuthModal={auth.showAuthModal}
            authMode={auth.authMode}
            openAuthModal={auth.openAuthModal}
            closeAuthModal={auth.closeAuthModal}
            handleAuthSuccess={auth.handleAuthSuccess}
          />
          <button
            className="relative p-2 text-white hover:text-gray-300 focus:outline-none"
            onClick={togglePanel}
          >
            <BellIcon className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-600 rounded-full">
              3
            </span>
          </button>
        </div>
      </div>
    </div>
  </header>
);

export default Navbar;
