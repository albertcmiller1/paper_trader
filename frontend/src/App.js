
import React from 'react';
import { Routes, Route} from 'react-router-dom';

import Navigation     from './components/Navbar'
import HomePage       from './pages/HomePage';
import PlotPage       from './pages/PlotPage';
import TradePage      from './pages/TradePage';
import PortfolioPage  from './pages/PortfolioPage';
import NotFoundPage   from './pages/NotFoundPage';

const App = () => {
  return (
    <div>
      <Navigation/>
      <Routes>
        <Route index                element={<HomePage/>}/>
        <Route path="/home"         element={<HomePage/>}/>
        <Route path="/plot"         element={<PlotPage/>}/>
        <Route path="/trade"        element={<TradePage/>}/>
        <Route path="/portfolio"    element={<PortfolioPage/>}/>
        <Route path="*"             element={<NotFoundPage/>}/>
      </Routes>
    </div>
  );
}

export default App;