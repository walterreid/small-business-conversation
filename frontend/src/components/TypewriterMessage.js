import React, { useState, useEffect, useRef } from 'react';

/**
 * TypewriterMessage Component
 * 
 * Displays text with a smooth typewriter effect, character by character.
 * Supports HTML content and maintains proper formatting.
 * 
 * Props:
 * - text: The text to display (can include HTML)
 * - speed: Typing speed in milliseconds per character (default: 20)
 * - onComplete: Callback when typing is complete
 * - skipTyping: If true, displays text immediately without typing effect
 */
function TypewriterMessage({ text, speed = 20, onComplete, skipTyping = false }) {
  const [displayedText, setDisplayedText] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const indexRef = useRef(0);
  const timeoutRef = useRef(null);

  useEffect(() => {
    if (!text) {
      setDisplayedText('');
      setIsComplete(false);
      return;
    }

    // If skipTyping is true, display immediately
    if (skipTyping) {
      setDisplayedText(text);
      setIsComplete(true);
      if (onComplete) {
        onComplete();
      }
      return;
    }

    // Reset state
    setDisplayedText('');
    setIsComplete(false);
    indexRef.current = 0;

    // Function to type next character
    const typeNextChar = () => {
      if (indexRef.current < text.length) {
        const remainingText = text.substring(indexRef.current);
        
        // If we're about to enter an HTML tag, skip to the end of the tag immediately
        if (remainingText.startsWith('<')) {
          const tagEnd = remainingText.indexOf('>');
          if (tagEnd !== -1) {
            // Include the entire tag at once (no delay for HTML tags)
            setDisplayedText(text.substring(0, indexRef.current + tagEnd + 1));
            indexRef.current = indexRef.current + tagEnd + 1;
            // Continue immediately for HTML tags
            timeoutRef.current = setTimeout(typeNextChar, 0);
          } else {
            // Malformed tag, just add one character
            setDisplayedText(text.substring(0, indexRef.current + 1));
            indexRef.current++;
            timeoutRef.current = setTimeout(typeNextChar, speed);
          }
        } else {
          // Regular character, add one at a time with typing speed
          setDisplayedText(text.substring(0, indexRef.current + 1));
          indexRef.current++;
          timeoutRef.current = setTimeout(typeNextChar, speed);
        }
      } else {
        // Typing complete
        setIsComplete(true);
        if (onComplete) {
          onComplete();
        }
      }
    };

    // Start typing after a short delay
    timeoutRef.current = setTimeout(typeNextChar, 100);

    // Cleanup on unmount or text change
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [text, speed, onComplete, skipTyping]);

  // Render with HTML support
  if (displayedText.includes('<')) {
    return <div dangerouslySetInnerHTML={{ __html: displayedText }} />;
  }

  return <div>{displayedText}</div>;
}

export default TypewriterMessage;

