import { useEffect, useState } from 'react';

interface AnimatedHeadingProps {
  text: string;
  className?: string;
  charDelay?: number;
  initialDelay?: number;
}

export default function AnimatedHeading({
  text,
  className = '',
  charDelay = 30,
  initialDelay = 200,
}: AnimatedHeadingProps) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimate(true), initialDelay);
    return () => clearTimeout(timer);
  }, [initialDelay]);

  const lines = text.split('\n');

  let globalIndex = 0;

  return (
    <h1 className={className} style={{ letterSpacing: '-0.04em' }}>
      {lines.map((line, lineIndex) => {
        const lineStartIndex = globalIndex;
        const chars = line.split('');

        const lineElements = chars.map((char, charIndex) => {
          const delay = (lineStartIndex + charIndex) * charDelay;
          globalIndex++;

          return (
            <span
              key={`${lineIndex}-${charIndex}`}
              className="inline-block transition-all duration-500"
              style={{
                opacity: animate ? 1 : 0,
                transform: animate ? 'translateX(0)' : 'translateX(-18px)',
                transitionDelay: `${delay}ms`,
              }}
            >
              {char === ' ' ? '\u00A0' : char}
            </span>
          );
        });

        // After processing this line, update globalIndex
        // (already done in the loop above)

        return (
          <span key={lineIndex} className="block">
            {lineElements}
          </span>
        );
      })}
    </h1>
  );
}
