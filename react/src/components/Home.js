import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import axios from 'axios';
import '../static/Home.scss';
import {createMessageElement, createPlaylistElement, createResetDiv} from './ElementCreator';
import Shared from './Shared';
import Loading from './Loading';
import Elipses from './Elipses';

function Home() {
  const [displayName, setDisplayName] = useState('');
  const [userInput, setUserInput] = useState('');
  const [askFor, setAskFor] = useState(['user_mood_occasion', 'artist_names', 'playlist_name']);
  const [playlistDetails, setPlaylistDetails] = useState({
        userMoodOccasion:"",
        artistNames:null,
        playlistName:""
      });
  const [AIResponse, setAIResponse] = useState(null);
  const messageContainerRef = useRef(null);
  const lastMessageRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [typing, setTyping] = useState(true);
  const [playlistUrl, setPlaylistUrl] = useState('');
  const regex = /.*[a-zA-Z]+.*/;
  const [userPic, setUserPic] = useState('');
  const [greeted, setGreeted] = useState(false);
  const [resetClicked, setResetClicked] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [buttonRef, setButtonRef] = useState(null);
  useEffect(() => {
    axios
      .get('/get_display_name')
      .then((response) => {
        setDisplayName(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error: ', error);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    axios
      .get('/get_user_pic')
      .then((response) => {
        setUserPic(response.data)
      })
      .catch((error) => {
        console.error('Error: ', error);
      });
  }, []);

  useLayoutEffect(() => {
    if (!loading && messageContainerRef.current) {

      axios.post('/get_greeting_message', {
        display_name: displayName,
      })
      .then((response) => {

        setAIResponse(response.data['greetingMessage']);
        const greetingAI= createMessageElement(response.data['greetingMessage'], "message-AI", userPic);
        messageContainerRef.current.appendChild(greetingAI);

        setGreeted(true);

      })
      .catch((error) => {
        console.error('Error: ', error);

      });

    }
  }, [loading]);

  useLayoutEffect(() => {
    initialQuestion();
    setTyping(false);
  }, [greeted]);

  useEffect(() => {
    setTyping(true);
    if (resetClicked && !disabled){
      initialQuestion()
      setTyping(false);
      setDisabled(true);
      //setResetClicked(false);
      console.log(typeof(buttonRef));
      //buttonRef.disabled = true;
    }
    console.log(disabled);
    console.log(resetClicked);
  },[resetClicked])

  const initialQuestion = () =>{
    if (!loading && messageContainerRef.current) {
      axios
      .get('/get_initial_question')
      .then((response) => {

        setAIResponse(response.data['initialQuestion']);
        const questionAI= createMessageElement(response.data['initialQuestion'], "message-AI", userPic);

        messageContainerRef.current.appendChild(questionAI);

      })
      .catch((error) => {
        console.error('Error: ', error);
      },[]);

    }
  };

  useEffect(() => {
    lastMessageRef.current?.scrollIntoView();
  }, [userInput, playlistUrl, typing, messageContainerRef]);

  function generatePlaylist(currPlaylistDetails){
    axios.post('/generate_playlist', {
      playlist_details: currPlaylistDetails
    }).then((response) => {

      if(response.data['AIResponse'] !== "True"){
        const messageElementAI= createMessageElement(response.data['AIResponse'], "message-AI", userPic);
        messageContainerRef.current.appendChild(messageElementAI);
      }
      
      const playlistID = response.data['playlistID']
      const playlistElement = createPlaylistElement(playlistID, "message-AI")
      messageContainerRef.current.appendChild(playlistElement);
      setPlaylistUrl(response.data['playlistUrl'])
      const resetDict = createResetDiv(reset);
      const resetElement = resetDict['resetElement'];
      const button = resetDict['button'];
      messageContainerRef.current.appendChild(resetElement);
      setButtonRef(button)
    })
  }

  function reset(){
    setAskFor(['user_mood_occasion', 'artist_names', 'playlist_name']);
    setPlaylistDetails({
      userMoodOccasion:"",
      artistNames:null,
      playlistName:""
    });
    setResetClicked(true);
    setDisabled(false);
  }
  
  const handleSubmit = async (event) => {
    setTyping(true);
    event.preventDefault();
    try {
      //sending the user input, ask list, and playlist details to backend
      if(userInput && regex.test(userInput)){

        await axios.post('/get_user_input', {
          user_input: userInput,
          ask_for: askFor,
          p_details: playlistDetails,
          ai_response: AIResponse
        }).then((response) => {

          setAskFor(response.data['updatedAskList']);
          setPlaylistDetails(response.data['updatedPlaylistDetails']);
          setAIResponse(response.data['AIResponse']);

          const currAskfor = response.data['updatedAskList'];
          const currPlaylistDetails = response.data['updatedPlaylistDetails'];
  
          const messageElementUser = createMessageElement(userInput, "message-user", userPic);
          messageContainerRef.current.appendChild(messageElementUser);
        
          const messageElementAI= createMessageElement(response.data['AIResponse'], "message-AI", userPic);
          messageContainerRef.current.appendChild(messageElementAI);
          
          if(currAskfor.length === 0 && currPlaylistDetails["userMoodOccasion"] != null){
            generatePlaylist(currPlaylistDetails);
          }
          else{
            setTyping(false);
          }
        });
        //resetting user input in prep for next submit 
        setUserInput('');
      }
      
    } catch (error) {
      console.error('Error sending data:', error);
    }
  }

  return (
    <div className="App">
      <Shared></Shared>
      {loading ? (
        <Loading />
      ) : (
        <div>
          <div className="text-container">
            <header>
              <h1 className="home-greeting">Welcome {displayName}</h1>
            </header>
            <div className="chat-top-bar">
              <div id="text">Groova</div>
            </div>
            <div className="chat-box">
              <div className="message-cont" ref={messageContainerRef}></div>
                {typing && (<div className="elipses">{<Elipses typing={typing} />}</div>)}
              <div ref={lastMessageRef}></div>
            </div>
            <form onSubmit={handleSubmit} className="form-container">
              <input
                placeholder="Aa"
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                className="input-bar"
              />
                <button type="submit" className="submit-button" disabled={typing}>
                <img id="send-icon" src={typing ? require('../images/pause.png') : require('../images/send_icon_groova.png')} alt="send button icon"/>
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
  
}

export default Home;