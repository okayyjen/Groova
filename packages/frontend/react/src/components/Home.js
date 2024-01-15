import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import axios from 'axios';
import '../static/Home.scss';
import {createMessageElement, createPlaylistElement } from './ElementCreator';
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
  const [loading, setLoading] = useState(true);
  const [typing, setTyping] = useState(true);
  const [pause, setPause] = useState(true);
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [userPic, setUserPic] = useState('');
  const [greeted, setGreeted] = useState(false);
  const [playlistComplete, setPlaylistComplete] = useState(false);
  const messageContainerRef = useRef(null);
  const lastMessageRef = useRef(null);
  const regex = /.*[a-zA-Z]+.*/;

  useEffect(() => {
    axios
      .get('/api/get_display_name', {withCredentials:true})
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
      .get('/api/get_user_pic', {withCredentials:true})
      .then((response) => {
        setUserPic(response.data)
      })
      .catch((error) => {
        console.error('Error: ', error);
      });
  }, []);

  useLayoutEffect(() => {
    if (!loading && messageContainerRef.current) {

      axios.post('/api/get_greeting_message', {
        display_name: displayName,
      }, {withCredentials:true})
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

  useEffect(() => {
    lastMessageRef.current?.scrollIntoView();
  }, [userInput, playlistUrl, typing, messageContainerRef, AIResponse]);

  const initialQuestion = async () =>{
    
    if (!loading && messageContainerRef.current) {
      axios
      .get('/api/get_initial_question', {withCredentials:true})
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

  function generatePlaylist(currPlaylistDetails){
    axios.post('/api/generate_playlist', {
      playlist_details: currPlaylistDetails
    }, {withCredentials:true}).then((response) => {

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
    setPlaylistComplete(false);
  }
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      //sending the user input, ask list, and playlist details to backend
      if(userInput && regex.test(userInput)){
        setTyping(true);
        setPause(true);
        const messageElementUser = createMessageElement(userInput, "message-user", userPic);
        messageContainerRef.current.appendChild(messageElementUser);
        //resetting user input in prep for next submit 
        setUserInput('');

        await axios.post('/api/get_user_input', {
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
          const text = response.data['AIComment'] + " " + response.data['AIResponse']
          const messageElementAI= createMessageElement(text, "message-AI", userPic);
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
            <div className="chat-wrapper">
                <div className="chat-box">
                <div className="message-cont" ref={messageContainerRef}></div>
                  {playlistComplete && (<ResetButton onClick = {reset} ></ResetButton>)}
                  {typing && (<div className="elipses">{<Elipses/>}</div>)}
                <div ref={lastMessageRef}></div>
              </div>
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