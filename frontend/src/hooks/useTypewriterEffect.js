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
          let letter_message = text[index];
          setDisplayedText(prev => prev + letter_message);
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