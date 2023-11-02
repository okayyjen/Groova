import React from 'react';
import Shared from './Shared';
import '../static/Loading.scss';

const Loading = () => {
  return (
    <div className="lds-ring"><div></div><div></div><div></div><div></div></div>
  );
};

export default Loading;