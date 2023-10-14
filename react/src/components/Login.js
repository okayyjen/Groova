import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Shared from './Shared';


function Login() {
  const [url, setUrl] = useState('ERRA');

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
      <Shared></Shared>
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