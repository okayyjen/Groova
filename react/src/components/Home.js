import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.scss';
import '../Home.scss';

function Home() {
  const [curX, setCurX] = useState(0);
  const [curY, setCurY] = useState(0);
  const [displayName, setDisplayName] = useState('');
  const [userInput, setUserInput] = useState('')
  const [askFor, setAskFor] = useState(['playlist_name', 'artist_name', 'user_mood_occasion'])
  const [playlistDetails, setPlaylistDetails] = useState({
    playlistName:"",
    artistName:"",
    userMoodOccasion:""})
  const [AIResponse, setAIResponse] = useState('error while retrieving AI response')

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
    axios
      .get('/get_display_name')
      .then((response) => {
        setDisplayName(response.data);
      })
      .catch((error) => {
        console.error('Error: ', error);
      });
  }, []);


  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      //sending the user input, ask list, and playlist details to backend
      const response = await axios.post('/get_user_input', {
        user_input: userInput,
        ask_for: askFor,
        p_details: playlistDetails
      });

      console.log('Handling server response:', response.data);
      
      setAskFor(response.data['updatedAskList']);
      setPlaylistDetails(response.data['updatedPlaylistDetails']);
      setAIResponse(response.data['AIResponse']);
      
      //resetting user input in prep for next submit 
      setUserInput('');
    } catch (error) {
      console.error('Error sending data:', error);
    }

  }

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
              <h1 className = "home-greeting">Welcome to the Harb Kim Empire {displayName}</h1>
            </header>
            <div className = "chat-box">
              <form onSubmit={handleSubmit} className='form-container'>
                <input 
                  placeholder='Aa'
                  type="text" 
                  value={userInput} 
                  onChange={(e) => setUserInput(e.target.value)}
                  className="input-bar"
                  />
                <button type="submit" className="submit-button"/>
              </form>
            </div>
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

export default Home;