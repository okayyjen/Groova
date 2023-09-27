import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Home from './Home'; 

function App() {
  const [url, setUrl] = useState('bitch');
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
          <button onClick={() => window.location.href = url}>login with dookify</button>
      </div>
  );
}

export default App;