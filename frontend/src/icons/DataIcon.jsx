import React from 'react';

export default function DataIcon(props) {
  return (
    <svg
      {...props}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Database icon, style matches HomeIcon, from https://www.w3.org/TR/SVG2/ */}
      <ellipse cx="12" cy="6.5" rx="8" ry="3.5" fill="currentColor"/>
      <path d="M4 6.5v11c0 1.93 3.58 3.5 8 3.5s8-1.57 8-3.5v-11" fill="none" stroke="currentColor" strokeWidth="2"/>
      <ellipse cx="12" cy="17.5" rx="8" ry="3.5" fill="currentColor" fillOpacity="0.5"/>
      <ellipse cx="12" cy="12" rx="8" ry="3.5" fill="currentColor" fillOpacity="0.7"/>
    </svg>
  );
}
