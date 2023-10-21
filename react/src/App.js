import React, { useEffect } from 'react';
import './static/App.scss';
import { Route, Routes} from 'react-router-dom';

import Home from './components/Home';
import Login from './components/Login';
import WebFont from 'webfontloader';

export function App() {
  useEffect(() => {
    WebFont.load({
      google: {
        families: ['Chango', 'Chilanka']
      }
    });
   }, []);
    return (
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    )
  }

export default App;