import React from 'react';
import './MainPage.css';
import { Link } from 'react-router-dom';

const MainPage = () => {
  return (
    <div className="main-page">
    <div className='container'>
      <h2>Welcome to the Home Page!</h2>
      <Link to="/recognize" className='button-container'>
        <button>Go to Recognize</button>
      </Link>
      <Link to="/addface" className='button-container'>
        <button>Go to AddFace</button>
      </Link>
    </div>
    </div>
  );
};

export default MainPage;