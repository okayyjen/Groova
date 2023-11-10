import React from 'react';
import '../static/Loading.scss';

function Elipses({ typing }){
  return (
    <div className="dots" style={{animation: typing ? 'overall-scale 8000s infinite' : 'overall-scale 5s infinite',}}>
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );
};

export default Elipses;