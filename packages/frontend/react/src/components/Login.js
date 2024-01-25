import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Shared from './Shared';
import '../static/Login.scss';
import { io } from 'socket.io-client';

let socket;

function Login() {
  const [url, setUrl] = useState('ERRA');
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([])

  useEffect(() => {

    // create websocket
    socket = io();
    
    // listen for chat events
    socket.on("chat", (chat) => {
        // when we recieve a chat, add it into our messages array in state
        setMessages(messages => [...messages, chat])
    })
    
    // when component unmounts, disconnect
    return (() => {
        socket.disconnect()
    })
  }, [])

  useEffect(() => {
    axios.get('/api/login', {withCredentials:true})
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
              <h1 id= "logo-text">Groovify</h1>
          </header>
          <p id = "subtext">Connect your Spotify account to get started</p>
          <div id = "btn-container">
            <button className="Btn" onClick={() => window.location.href = url}>
                <div id = "btn-contents">
                  <p className="text">Login With </p>
                  <img id = "spotify-logo" src={require('../images/spotify_logo.png')} alt = "spotify logo"/>
                </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;