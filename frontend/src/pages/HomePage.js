import React from "react";
 
import LiveChart from '../charts/LiveChart';

const HomePage = () => {
    return (
        <div>
            <center>
            <h1>
                Paper Trader | Home
            </h1>
            </center>
            <LiveChart/>
        </div>
    );
};

export default HomePage;