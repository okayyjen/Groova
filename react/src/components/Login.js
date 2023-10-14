import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Shared from './Shared';


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
      <Shared  curX={curX} curY={curY}></Shared>
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
      </div>
    </div>
  );
  
}

export default Login;