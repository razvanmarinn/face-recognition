import React from 'react';
import { Link } from 'react-router-dom';
import './css/Navbar.css';
import { FaUser } from "react-icons/fa";

const Navbar = () => {
    return (
        <nav className="menu">
            <div className="navbar-content">
                <img className="logo" src={process.env.PUBLIC_URL + '/noun-face-recognition-1903274.png'} alt="logo" />
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/recognize">Recognize</Link></li>
                    <li><Link to="/addface">Add Face</Link></li>
                    <li><Link to="/shared_image_pool">Shared Image Pool</Link></li>
                    <li><Link to="/browse_faces">Browse Faces</Link></li>
                </ul>
                <div class="right-container">
                <form action="submit" className="Search-form">
                    <div className="Search-inner">
                        <input type="search" id="SearchInput" placeholder="Search"/>
                        <label className="Label" htmlFor="SearchInput"></label>  
                    </div>
                </form>
                <div className="icon-right">
                <Link to="/profile" style={{ color: '#fff' }} activeStyle={{ color: '#66c4c4' }}><FaUser size={30} /></Link>
                </div>

            </div>
            </div>
        </nav>
    );
}

export default Navbar;