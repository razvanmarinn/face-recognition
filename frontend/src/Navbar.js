import React from 'react';
import { Link } from 'react-router-dom';
import './css/Navbar.css';

const Navbar = () => {
    return (
        <nav className="menu">
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/recognize">Recognize</Link></li>
                <li><Link to="/addface">Add Face</Link></li>
                <li><Link to="/shared_image_pool">Shared Image Pool</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;