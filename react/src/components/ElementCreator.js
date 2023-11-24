export function createMessageElement(input, divName, profile) {
    const messageElement = document.createElement('div');
    const textElement = document.createElement('div');
    const aiProfile = document.createElement("IMG");
    const aiElement = document.createElement('div');
    const userProfile = document.createElement("IMG");
    const userElement = document.createElement('div');

    aiProfile.setAttribute('src', require('../images/groova_pfp.png'));
    aiProfile.setAttribute('id', "profile-ai");


    const imageSource = profile === "no pfp" ? require('../images/default_pfp.png') : profile;

    userProfile.setAttribute('src', imageSource);
    userProfile.setAttribute('id', "profile-user");    
    textElement.textContent = input;
    textElement.id = "message-text";

    messageElement.appendChild(textElement);
    messageElement.innerHTML = messageElement.innerHTML.replace(/([\uD800-\uDBFF][\uDC00-\uDFFF])/g, '<span id="emoji-container">$1</span>')
    messageElement.id = divName;

    if(divName==="message-user"){
        userElement.id = "div-user";
        userElement.appendChild(messageElement);
        userElement.appendChild(userProfile);
        return userElement;
    }
    else if(divName === "message-AI"){
        aiElement.id = "div-ai";
        aiElement.appendChild(aiProfile);
        aiElement.appendChild(messageElement);
        return aiElement;
    }
}

export function createPlaylistElement(playlistID, divName){
    const messageElement = document.createElement('div');
    const playlistElement = document.createElement('iframe');
    const aiProfile = document.createElement("IMG");
    const aiElement = document.createElement('div');
    aiProfile.setAttribute('src', require('../images/groova_pfp.png'));
    aiProfile.setAttribute('id', "profile-ai");

    playlistElement.setAttribute('style', "border-radius:40px 40px 40px 10px");
    playlistElement.setAttribute('src', "https://open.spotify.com/embed/playlist/" + playlistID + "?utm_source=generator");
    playlistElement.setAttribute('width', "100%");
    playlistElement.setAttribute('height', "352px");
    playlistElement.setAttribute('frameBorder', "0");
    playlistElement.setAttribute('allowfullscreen', "");
    playlistElement.setAttribute('allow', "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture");
    playlistElement.setAttribute('loading', "lazy");

    messageElement.appendChild(playlistElement);
    messageElement.id = "playlist-display";
    aiElement.id = "div-playlist";
    aiElement.appendChild(aiProfile);
    aiElement.appendChild(messageElement);
    return aiElement;
}

export function createResetMessage(){
    const messageElement = document.createElement('div');
    const button = document.createElement('button');
    const buttonPic = document.createElement("IMG");
    button.setAttribute('type', "button");
    button.setAttribute('id', "reset-btn");

    buttonPic.setAttribute('src', require('../images/reset.png'));
    button.appendChild(buttonPic);

    const textElement = document.createElement('div');
    textElement.textContent = "would you like to reset?";
    textElement.id = "message-text";

    const aiProfile = document.createElement("IMG");
    const aiElement = document.createElement('div');
    aiProfile.setAttribute('src', require('../images/groova_pfp.png'));
    aiProfile.setAttribute('id', "profile-ai");

    messageElement.appendChild(textElement);
    messageElement.appendChild(button);
    messageElement.id = "message-AI";

    aiElement.id = "div-ai";
    aiElement.appendChild(aiProfile);
    aiElement.appendChild(messageElement);


    return aiElement;


}