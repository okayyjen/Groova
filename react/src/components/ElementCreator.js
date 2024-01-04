export function createMessageElement(input, divName, profile) {
    const messageElement = document.createElement('div');
    const textElement = document.createElement('div');
    const aiProfile = document.createElement("IMG");
    const aiElement = document.createElement('div');
    const userProfile = document.createElement("IMG");
    const userElement = document.createElement('div');

    aiProfile.setAttribute('src', require('../images/groova_pfp.png'));
    aiProfile.id ="profile-ai";

    const imageSource = profile === "no pfp" ? require('../images/default_pfp.png') : profile;

    userProfile.src = imageSource;
    userProfile.id ="profile-user";  

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

export function createPlaylistElement(playlistID){
    const messageElement = document.createElement('div');
    const playlistElement = document.createElement('iframe');
    const aiProfile = document.createElement("IMG");
    const aiElement = document.createElement('div');
    aiProfile.setAttribute('src', require('../images/groova_pfp.png'));
    aiProfile.id = "profile-ai";
    playlistElement.id ='playlist-element';

    playlistElement.setAttribute('src', "https://open.spotify.com/embed/playlist/" + playlistID + "?utm_source=generator");
    playlistElement.allowfullscreen = "";
    playlistElement.setAttribute('allow', "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture");
    playlistElement.loading = "lazy";

    messageElement.appendChild(playlistElement);
    messageElement.id = "playlist-display";
    aiElement.id = "div-playlist";
    aiElement.appendChild(aiProfile);
    aiElement.appendChild(messageElement);
    return aiElement;
}

