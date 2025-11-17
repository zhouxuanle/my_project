import React from 'react';

export default function TableIcon(props) {
  // props allow className, width, height, aria-hidden, etc.
  return (
    <svg
      {...props}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" strokeWidth="1.4" fill="none" />
      <path d="M3 8.5h18" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M9.5 8.5v11" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M15.5 8.5v11" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M3 13.5h18" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.9" />
    </svg>
  );
}
