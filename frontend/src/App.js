
import React, { useState, useCallback, useEffect } from 'react';
import { Routes, Route} from 'react-router-dom';

import useWebSocket, { ReadyState } from 'react-use-websocket';
import Navigation     from './components/Navbar'
import HomePage       from './pages/HomePage';
import PlotPage       from './pages/PlotPage';
import TradePage      from './pages/TradePage';
import PortfolioPage  from './pages/PortfolioPage';
import NotFoundPage   from './pages/NotFoundPage';

const WS_URL = 'ws://0.0.0.0:5001/price';

const App = () => {
  
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
          var message = lastMessage.data.replace(/'/g, '"');
          const obj = JSON.parse(message)
          var newData = { x: parseFloat(obj.date_time), y: parseFloat(obj.curr_price) }
          setMessageHistory(messageHistory => [...messageHistory, newData]);
      }
  }, [lastMessage, setMessageHistory]);


  return (
    <div>
      <Navigation/>
      <Routes>
        <Route index                element={<HomePage liveStockData={messageHistory}/>}/>
        <Route path="/home"         element={<HomePage liveStockData={messageHistory}/>}/>
        <Route path="/plot"         element={<PlotPage/>}/>
        <Route path="/trade"        element={<TradePage/>}/>
        <Route path="/portfolio"    element={<PortfolioPage/>}/>
        <Route path="*"             element={<NotFoundPage/>}/>
      </Routes>
    </div>
  );
}

export default App;