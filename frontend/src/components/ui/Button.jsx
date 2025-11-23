import React from 'react';

const variants = {
  primary: `
    bg-app-dark border border-white/10 rounded-lg cursor-pointer 
    transition-all flex items-center
    px-5 py-4 hover:bg-app-hover hover:translate-x-1
  `,
  action: `
    w-full bg-white/10 hover:bg-white/20 border border-white/10 
    font-semibold py-3.5 px-6 rounded-lg transition-all 
    disabled:opacity-50 disabled:cursor-not-allowed uppercase tracking-wider text-sm
  `,
  table: `
    bg-app-dark text-white border border-white/10 rounded-lg cursor-pointer 
    transition-all duration-300 ease-in-out w-full h-16 text-base font-semibold 
    hover:scale-110 hover:shadow-lg hover:shadow-black/30
    flex justify-center items-center m-0
  `
};

const Button = ({ 
  children, 
  variant = 'primary', 
  className = '', 
  ...props 
}) => {
  const baseStyles = variants[variant] || variants.primary;
  
  return (
    <button 
      className={`${baseStyles} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
