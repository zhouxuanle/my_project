import React from 'react';

const variants = {
  circle: `
    bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-full
    w-16 h-16 shadow-lg shadow-purple-400/30 hover:scale-105
    flex items-center justify-center transition-transform duration-200
    md:w-20 md:h-20
  `,
  small: `
    bg-white/10 text-white rounded-full w-12 h-12 border border-white/10 shadow-sm
    hover:scale-105 hover:bg-white/20 hover:shadow-md
    flex items-center justify-center transition-transform duration-200
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-400/60
    md:w-14 md:h-14
  `
};

const MenuButton = ({ variant = 'small', children, className = '', ...props }) => {
  const baseStyles = variants[variant] || variants.small;
  
  return (
    <button 
      className={`${baseStyles} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default MenuButton;
