import React from 'react';

const PageTitle = ({ children, className = '' }) => {
  return (
    <h1 className={`text-4xl font-bold mb-8 text-white tracking-tight text-center ${className}`}>
      {children}
    </h1>
  );
};

export default PageTitle;
