import React, { useState, useEffect } from 'react';
import axios from 'axios';


function Login() {
  const [url, setUrl] = useState('ERRA');
  //get authURL from /login
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
    <div className="center-content">
      <header>
        <h1 className="font-loader">Groova</h1>
      </header>
      <p>Connect your Spotify account to get started</p>
      <button onClick={() => window.location.href = url}>Login with Spotify</button>
    </div>
    <div>
      <body>
        <section id="up"></section>
        <section id="down"></section>
        <section id="left"></section>
        <section id="right"></section>
      </body>
    </div>
  </div>
  );
}

export default Login;