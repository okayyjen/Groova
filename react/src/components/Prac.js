import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../Prac.scss';

function Prac() {
  const [curX, setCurX] = useState(0);
  const [curY, setCurY] = useState(0);

  useEffect(() => {
    const interBubble = document.querySelector(".interactive");
    
    // Center the interactive element initially
    const initialX = window.innerWidth / 2;
    const initialY = window.innerHeight / 2;
    setCurX(initialX);
    setCurY(initialY);

    const handleMouseMove = (event) => {
      setCurX(event.clientX);
      setCurY(event.clientY);
    };

    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []); // Empty dependency array ensures this effect runs only once

  return (
    <div className="App">
      <div>
        <div className="text-container">Bubbles</div>
        <div className="gradient-bg">
          <svg xmlns="http://www.w3.org/2000/svg">
            <defs>
              <filter id="goo">
                <feGaussianBlur
                  in="SourceGraphic"
                  stdDeviation="10"
                  result="blur"
                />
                <feColorMatrix
                  in="blur"
                  mode="matrix"
                  values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
                  result="goo"
                />
                <feBlend in="SourceGraphic" in2="goo" />
              </filter>
            </defs>
          </svg>
          <div className="gradients-container">
            <div className="g1"></div>
            <div className="g2"></div>
            <div className="g3"></div>
            <div className="g4"></div>
            <div className="g5"></div>
            <div
              className="interactive"
              style={{
                transform: `translate(${curX}px, ${curY}px)`,
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
  
}

export default Prac;