import React from 'react';

const Panel = ({ children, className = '' }) => {
  return (
    <div className={`bg-white/5 backdrop-blur-lg border border-white/10 p-8 rounded-2xl shadow-2xl flex flex-col gap-6 items-center w-full max-w-md mx-auto mb-10 transition-all hover:bg-white/[0.07] ${className}`}>
      {children}
    </div>
  );
};

export default Panel;
