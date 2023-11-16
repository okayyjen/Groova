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