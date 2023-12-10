import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import axios from 'axios';
import '../static/Home.scss';
import {createMessageElement, createPlaylistElement, createResetDiv, createResetDivComponent} from './ElementCreator';
import Shared from './Shared';
import Loading from './Loading';
import Elipses from './Elipses';
import ResetButton from './ResetButton';

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
  const [pause, setPause] = useState(true);
  const [playlistUrl, setPlaylistUrl] = useState('');
  const regex = /.*[a-zA-Z]+.*/;
  const [userPic, setUserPic] = useState('');
  const [greeted, setGreeted] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [playlistComplete, setPlaylistComplete] = useState(false);

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
  }, [greeted]);

  useEffect(() => {
    if(playlistComplete === true){
      setTyping(false);
    }
  }, [playlistComplete]);

  const initialQuestion = async () =>{
    
    if (!loading && messageContainerRef.current) {
      axios
      .get('/get_initial_question')
      .then((response) => {

        const questionAI= createMessageElement(response.data['initialQuestion'], "message-AI", userPic);
        messageContainerRef.current.appendChild(questionAI);
        setAIResponse(response.data['initialQuestion']);

        setTyping(false);
        setPause(false);

      })
      .catch((error) => {
        console.error('Error: ', error);
      },[]);

    }
  };

  useEffect(() => {
    lastMessageRef.current?.scrollIntoView();
  }, [userInput, playlistUrl, typing, messageContainerRef, AIResponse]);

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
      setPlaylistComplete(true);
    })
  }

  function reset(){
    setAskFor(['user_mood_occasion', 'artist_names', 'playlist_name']);
    setPlaylistDetails({
      userMoodOccasion:"",
      artistNames:null,
      playlistName:""
    });
    setTyping(true);
    initialQuestion();
    setDisabled(false);
    setPlaylistComplete(false);
  }
  
  const handleSubmit = async (event) => {
    setTyping(true);
    setPause(true);
    event.preventDefault();
    try {
      //sending the user input, ask list, and playlist details to backend
      if(userInput && regex.test(userInput)){

        const messageElementUser = createMessageElement(userInput, "message-user", userPic);
        messageContainerRef.current.appendChild(messageElementUser);
        //resetting user input in prep for next submit 
        setUserInput('');

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

          const messageElementAI= createMessageElement(response.data['AIResponse'], "message-AI", userPic);
          messageContainerRef.current.appendChild(messageElementAI);
          
          if(currAskfor.length === 0 && currPlaylistDetails["userMoodOccasion"] != null){
            generatePlaylist(currPlaylistDetails);
          }
          else{
            setTyping(false);
            setPause(false);
          }
        });
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
                {playlistComplete && (<ResetButton onClick = {reset} ></ResetButton>)}
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
                <button type="submit" className="submit-button" disabled={pause}>
                <img id="send-icon" src={pause ? require('../images/pause.png') : require('../images/send_icon_groova.png')} alt="send button icon"/>
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
  
}

export default Home;