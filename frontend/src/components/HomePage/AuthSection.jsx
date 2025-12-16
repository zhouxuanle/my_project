import React from 'react';
import Button from '../ui/Button';
import Modal from '../ui/Modal';
import Login from '../Login';
import Signup from '../Signup';

function AuthSection({ isLoggedIn, handleLogout, showAuthModal, authMode, openAuthModal, handleAuthSuccess }) {
  return (
    <>
      <div className="absolute top-4 right-4 flex gap-4 z-10">
        {isLoggedIn ? (
          <Button onClick={handleLogout}>Logout</Button>
        ) : (
          <>
            <Button onClick={() => openAuthModal('login')}>Login</Button>
            <Button onClick={() => openAuthModal('signup')}>Sign Up</Button>
          </>
        )}
      </div>
      <Modal 
        isOpen={showAuthModal} 
        onClose={() => {}} // Assuming modal handles close internally or pass prop if needed
        title={authMode === 'login' ? 'Login' : 'Sign Up'}
      >
        {authMode === 'login' ? (
          <Login onSuccess={handleAuthSuccess} switchToSignup={() => openAuthModal('signup')} />
        ) : (
          <Signup onSuccess={handleAuthSuccess} switchToLogin={() => openAuthModal('login')} />
        )}
      </Modal>
    </>
  );
}

export default AuthSection;