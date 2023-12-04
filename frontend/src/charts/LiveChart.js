import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import CanvasJSReact from '@canvasjs/react-charts';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

const WS_URL = 'ws://0.0.0.0:5001/price';

function LiveChart(props) {
  
    const [messageHistory, setMessageHistory] = useState([]);

    const options = {
        theme: 'dark',
        animationEnabled: true,
        title: {
        text: 'Live price data streaming from the order book',
        },
        data: [
        {
            type: 'line',
            dataPoints: messageHistory
        },
        ],
    }

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
            var idx = messageHistory.length
            var newData = { x: idx, y: parseFloat(lastMessage.data) }
            setMessageHistory(messageHistory => [...messageHistory, newData]);

            // let i = 0;
            // console.log("--------", messageHistory.length)
            // while (i < messageHistory.length) {
            //     console.log(messageHistory[i]);
            //     i++;
            // }
        }
    }, [lastMessage, setMessageHistory]);


    return (
        <div className="App">
        <CanvasJSChart options={options} />
        </div>
    );
}

export default LiveChart;
