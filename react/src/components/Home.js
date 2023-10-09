import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.scss';

function Home() {
  const [displayName, setDisplayName] = useState('');
  useEffect(() => {
    axios
      .get('/get_display_name')
      .then((response) => {
        setDisplayName(response.data);
      })
      .catch((error) => {
        console.error('Error: ', error);
      });
  }, []);


  return (
    <div className="App">
      <div className="homepage">
        <header>
          <h1>Welcome to the Harb Kim Empire {displayName}</h1>
        </header>
        <main>
          <form className="center-content" method="POST" action="/getinput">
            <label htmlFor="user_input">Enter text:</label>
            <input
              type="text"
              id="user_input"
              name="user_input"
            />
            <input type="submit" value="Submit" />
          </form>
        </main>
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

export default Home;