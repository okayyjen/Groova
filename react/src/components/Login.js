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
        <header>
            <h1>Groova</h1>
        </header>
        <p>Connect your spotify account to get started</p>
        <button onClick={() => window.location.href = url}>login with spotify</button>
      </div>
  );
}

export default Login;