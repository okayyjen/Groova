import React, { useState, useEffect } from 'react';
import axios from 'axios';

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

  const [inputValue, setInputValue] = useState(''); // State for the input value

  // Function to handle changes in the input field and update the inputValue state
  const handleInputChange = (e) => {
    
  };

  // Function to handle form submission and update the displayName state
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent the form from submitting and reloading the page
    
  };

  return (
    <div className="homepage">
      <header>
        <h1>Welcome to the Harb Kim Empire {displayName}</h1>
      </header>
      <main>
        <form method="POST" action="/getinput">
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
  );
}

export default Home;