import React from 'react';
import '../static/Loading.scss';

function Elipses({ children }){
  return (
    <div className="dots">
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );
};

export default Elipses;