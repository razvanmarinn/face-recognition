import React from 'react';
import './css/MainPage.css';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

const MainPage = () => {
  return (
    <div className="main-page">
      <Navbar />
      <div className='centered-content'>
        <div className='container'>
          <h2>Welcome to the Home Page!</h2>
          <Link to="/recognize" className='button'>
            <button>Go to Recognize</button>
          </Link>
          <Link to="/addface" className='button'>
            <button>Go to AddFace</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MainPage;