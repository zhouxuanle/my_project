import React from 'react';
import Button from '../ui/Button';
import Modal from '../ui/Modal';
import Login from './Login';
import Signup from './Signup';

function AuthSection({ 
  isLoggedIn, 
  handleLogout, 
  showAuthModal, 
  authMode, 
  openAuthModal, 
  closeAuthModal, 
  handleAuthSuccess 
}) {
  return (
    <>
      <div className="flex gap-4 items-center">
        {isLoggedIn ? (
          <Button 
            onClick={handleLogout}
            className="bg-app-dark border border-app-hover text-white hover:bg-app-hover px-4 py-2 rounded transition-colors"
          >
            Logout
          </Button>
        ) : (
          <>
            <Button 
              onClick={() => openAuthModal('login')}
              className="bg-app-dark border border-app-hover text-white hover:bg-app-hover px-4 py-2 rounded transition-colors"
            >
              Login
            </Button>
            <Button 
              onClick={() => openAuthModal('signup')}
              className="bg-app-dark border border-app-hover text-white hover:bg-app-hover px-4 py-2 rounded transition-colors"
            >
              Sign Up
            </Button>
          </>
        )}
      </div>

      <Modal 
        isOpen={showAuthModal} 
        onClose={closeAuthModal}
        title={authMode === 'login' ? 'Login' : 'Sign Up'}
      >
        {authMode === 'login' ? (
          <Login 
            onSuccess={handleAuthSuccess} 
            switchToSignup={() => openAuthModal('signup')} 
          />
        ) : (
          <Signup 
            switchToLogin={() => openAuthModal('login')} 
          />
        )}
      </Modal>
    </>
  );
}

export default AuthSection;
