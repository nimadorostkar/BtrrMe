import React, { useEffect, useState } from 'react';

const Chat = ({ roomName }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, data.message]);
        };

        return () => socket.close();
    }, [roomName]);

    const sendMessage = () => {
        const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);
        socket.onopen = () => {
            socket.send(JSON.stringify({ message: input }));
            setInput('');
        };
    };

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>{msg}</p>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chat;
