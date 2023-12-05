import React from "react";
import LiveChart from '../charts/LiveChart';

const HomePage = (props) => {
    return (
        <div>
            <center>
            <h1>
                Paper Trader | Home
            </h1>
            </center>
            <LiveChart liveData = {props.liveStockData}/>
        </div>
    );
};

export default HomePage;