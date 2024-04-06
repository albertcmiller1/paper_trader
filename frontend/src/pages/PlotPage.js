import React, { useState, useCallback, useEffect } from 'react';
import { Button } from 'reactstrap';
import LiveChart from '../charts/LiveChart';

const PlotPage = (props) => {
    const [stockHistory, setStockHistory] = useState([]);
    const fetchUserData = () => {
      fetch("http://127.0.0.1:5000/prices")
        .then(response => {
          return response.json()
        })
        .then(data => {
            var stocks = []
            for (var i = 0; i < data.length; i++) {
                stocks.push(
                    { 
                        x: parseFloat(data[i][0]), 
                        y: parseFloat(data[i][2]) 
                    }
                )
            }
            // stocks.sort(function(a,b) {return b.x - a.x});
            setStockHistory(stocks)
        })
    }

    useEffect(() => {
        fetchUserData();
     }, []);

    return (
        <div>
            <center>
            <h1>
                Paper Trader | Plot
            </h1>
            <Button onClick={fetchUserData} color="danger">Update!</Button>
            <LiveChart liveData = {stockHistory}/>
            </center>
        </div>
    );
};

export default PlotPage;