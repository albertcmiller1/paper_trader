import React from 'react';
import CanvasJSReact from '@canvasjs/react-charts';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

function LiveChart(props) {
    const options = {
        theme: 'dark',
        animationEnabled: true,
        title: {
            text: 'Live price data streaming from the order book',
        },
        data: [
            {
                type: 'line',
                dataPoints: props.liveData
            },
        ]
    }

    return (
        <div className="App">
        <CanvasJSChart options={options} />
        </div>
    );
}

export default LiveChart;
