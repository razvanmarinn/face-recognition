import React from 'react';
import './css/MainPage.css';
import Navbar from './Navbar';

const MainPage = () => {
  return (
    <div>
      <Navbar />
      <div className="wrapper">
        <div className="container">
          <h2>Welcome back to the Facial Recognition system!</h2>
          <p>Explore the features of our facial recognition technology designed to enhance your experience with seamless and secure authentication.</p>

          <h2>Key Features</h2>
          <ul>
            <li>Quick and secure authentication</li>
            <li>Personalized user experiences based on your preferences</li>
            <li>Enhanced privacy measures for your peace of mind</li>
          </ul>

          <h2>How It Works</h2>
          <p>Our advanced facial recognition system employs cutting-edge algorithms to analyze unique facial features, ensuring precise and swift identification without compromising your privacy.</p>

          <h2>Customize Your Experience</h2>
          <p>Explore settings to tailor your facial recognition experience. Adjust sensitivity and preferences to match your needs and preferences.</p>

          <h2>Ready to Explore?</h2>
          <p>Continue enjoying the benefits of facial recognition technology. Should you have any questions or need assistance, our support team is here to help.</p>
        </div>

        <div className="footer">
          <p>© {new Date().getFullYear()} Marin Razvan Cristian. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
