import { useState, useEffect } from 'react';

// Custom hook for typewriter effect
export function useTypewriterEffect(text, speed = 50) {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    if (text) {
      setDisplayedText('');
      let index = 0;
      const timer = setInterval(() => {
        if (index < text.length) {
          setDisplayedText(prev => prev + text[index]);
          index++;
        } else {
          clearInterval(timer);
        }
      }, speed);
      return () => clearInterval(timer);
    }
  }, [text, speed]);

  return displayedText;
}