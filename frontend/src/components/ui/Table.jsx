import React from 'react';

export const TableContainer = ({ children, className = '' }) => {
  return (
    <div className={`mx-auto p-dynamic bg-white/10 rounded-lg w-[90%] overflow-hidden max-h-[calc(100vh-100px)] ${className}`}>
      {children}
    </div>
  );
};

export const Table = ({ children, className = '', ...props }) => {
  return (
    <table className={`w-full border-collapse my-dynamic bg-white/5 rounded-lg ${className}`} {...props}>
      {children}
    </table>
  );
};

export const Thead = ({ children }) => (
  <thead className="bg-white/10">
    {children}
  </thead>
);

export const Th = ({ children }) => (
  <th className="p-dynamic text-left font-semibold text-white border-b border-white/10 sm:p-3 sm:text-xs md:p-4 md:text-sm">
    {children}
  </th>
);

export const Tbody = ({ children }) => (
  <tbody>
    {children}
  </tbody>
);

export const Tr = ({ children }) => (
  <tr className="transition-colors duration-200 hover:bg-white/[0.08]">
    {children}
  </tr>
);

export const Td = ({ children }) => (
  <td className="p-dynamic border-b border-white/10 text-dynamic-sm truncate whitespace-nowrap max-w-[80px] break-words sm:p-2 sm:text-[9px] md:p-3 md:text-xs last:border-b-0">
    {children}
  </td>
);
