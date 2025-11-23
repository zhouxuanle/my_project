import React from 'react';

const InputGroup = ({ label, id, ...props }) => {
  return (
    <div className="flex items-center justify-between w-full bg-black/20 rounded-lg p-2 focus-within:border-white/20 focus-within:bg-black/30">
      <label htmlFor={id} className="text-sm font-medium text-gray-300 ml-3 whitespace-nowrap">
        {label}
      </label>
      <input
        id={id}
        className=" bg-transparent border-none text-right text-xl font-bold p-2"
        {...props}
      />
    </div>
  );
};

export default InputGroup;
