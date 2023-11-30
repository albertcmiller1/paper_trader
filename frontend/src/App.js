import './App.css';
import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://0.0.0.0:5001/price';

function App() {
  
  const [messageHistory, setMessageHistory] = useState([]);

  const {
    sendMessage,
    sendJsonMessage,
    lastMessage,
    lastJsonMessage,
    readyState,
    getWebSocket,
  } = useWebSocket(WS_URL, {
    onOpen: () => console.log('opened'),
    // Will attempt to reconnect on all close events, such as server shutting down
    shouldReconnect: (closeEvent) => false,
  });


  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));

      let i = 0;
      console.log("--------", messageHistory.length)
      while (i < messageHistory.length) {
          console.log(messageHistory[i].data);
          i++;
      }
    }
  }, [lastMessage, setMessageHistory]);

  return (
    <div className="App">
     hello world

     <ul>
        {messageHistory.map((message, idx) => (
          <span key={idx}>{message ? message.data : null}</span>
        ))}
      </ul>
    </div>
  );
}

export default App;
