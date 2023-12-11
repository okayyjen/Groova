import React from 'react';

const ResetButton = ({onClick }) => {
  return (
    <div id = "reset-element">
      <button id = "reset-btn" onClick={onClick} >
        <p id = "btn-text">Create New Playlist</p>
      </button>
    </div>
  );
};

export default ResetButton;