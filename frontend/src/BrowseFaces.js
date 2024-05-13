import React, { useState } from 'react';
import './css/BrowseFaces.css';
import Navbar from './Navbar';

const BrowseFaces = () => {
  const [search, setSearch] = useState('');
  const [pictures, setPictures] = useState([]);

  const fetchPictures = async (searchValue) => {
    try {
      const jwt = localStorage.getItem('token_payload');
      const response = await fetch(`http://127.0.0.1:8000/face_recognition/get_faces/${searchValue}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${jwt}`,
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setPictures(data);
      console.log(data); 
    } catch (error) {
      console.error('Error fetching pictures:', error);
    }
  };

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
  };

  const handleSearch = () => {
    fetchPictures(search);
  };

  return (
    <div>
      <Navbar />
      <div className="browse-faces">
        <input
          type="text"
          value={search}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
        <button onClick={handleSearch}>Search</button>
        <div className="pictures-table">
          {pictures.map((pictureUrl, index) => (
            <div key={index} className="picture-row">
              <img src={pictureUrl} style={{width: '350px', height: '350px'}}/>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default BrowseFaces;