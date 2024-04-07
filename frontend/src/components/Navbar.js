import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/portfolio">Portfolio</Link>
        </li>
        <li>
          <Link to="/trade">Trade</Link>
        </li>
        <li>
          <Link to="/plot">Plot</Link>
        </li>
        <li>
          <Link to="/spread">Spread</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;