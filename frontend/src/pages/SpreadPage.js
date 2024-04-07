import React, { useState, useEffect } from "react";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { Table, Col } from 'reactstrap';

const WS_URL = 'ws://0.0.0.0:5001/spread';

const SpreadPage = (props) => {
    const [curSpread, setCurSpread] = useState([]); 
    
    const [buys, setBuys] = useState([]); 
    const [sells, setSells] = useState([]); 


    const {
        sendMessage,
        sendJsonMessage,
        lastMessage,
        lastJsonMessage,
        readyState,
        getWebSocket,
    } = useWebSocket(WS_URL, {
        onOpen: () => console.log('opened spread socket'),
        shouldReconnect: (closeEvent) => false,
    });

    useEffect(() => {
        if (lastMessage !== null) {
            const arr = lastMessage.data.split(" ")
            var buys = []
            var sells = []
            for (let i = 0; i < arr.length; i++) {
                if (arr[i]){
                    var cur_item = arr[i].split("-")
                    if (cur_item[1]=="buy") {
                        buys.push(Number(cur_item[0]))
                    }
                    if (cur_item[1]=="sell") {
                        sells.push(Number(cur_item[0]))
                    }
                }
            }
            setSells(sells.reverse())
            setBuys(buys.reverse())
        }
    }, [lastMessage, setCurSpread]);

    return (
        <div>
            <center>
            <h1>
                Paper Trader | Spread
            </h1>
            </center>
            <Col></Col>
            <Col>
                <Table>
                    <thead>
                        <tr>
                            <th>Trader Offer Type</th>
                            <th>Limit Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sells.map(sell_price => (
                        <tr className="table-danger">
                                <td>Ask</td>
                                <td>{sell_price}</td>
                            </tr>                       
                        ))}
                        {buys.map(buy_price => (
                        <tr className="table-success">
                                <td>Bid</td>
                                <td>{buy_price}</td>
                            </tr>                       
                        ))}
                    </tbody>
                </Table>
            
            </Col>
            <Col></Col>
        </div>
    );
};

export default SpreadPage;