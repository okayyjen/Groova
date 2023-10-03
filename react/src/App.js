import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes,Switch } from 'react-router-dom';

import Home from './components/Home';
import Login from './components/Login';

export function App() {
    return (
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    )
  }

export default App;