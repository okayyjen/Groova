export function createMessageElement(input, divName) {
    const messageElement = document.createElement('div');
    const textElement = document.createElement('div');
    

    textElement.textContent = input;
    textElement.id = "message-text";

    messageElement.appendChild(textElement);
    messageElement.id = divName
    return messageElement
}