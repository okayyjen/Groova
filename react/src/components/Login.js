import React, { useState, useEffect } from 'react';
import axios from 'axios';


function Login() {
  const [curX, setCurX] = useState(0);
  const [curY, setCurY] = useState(0);
  const [url, setUrl] = useState('ERRA');

  useEffect(() => {
    
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
  }, []);

  useEffect(() => {
    axios.get('/login')
        .then(response => {
            setUrl(response.data);
        })
        .catch(error => {
            console.error(error);
        });
}, []);

  return (
    <div className="App">
      <div>
        
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
          <div className = "text-container">
            <header>
                <h1 id= "logo_text">Groova</h1>
            </header>
            <p id = "subtext">Connect your Spotify account to get started</p>
            <button className="Btn" onClick={() => window.location.href = url}>
                <p className="text">Login With </p>
                <img id = "spotify_logo" src={require('../spotify_logo.png')} alt = "spotify logo"/>
            </button>
          </div>
          
          
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

export default Login;