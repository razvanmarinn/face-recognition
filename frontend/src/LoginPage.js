import React, { useState, useRef, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from './AuthContext';
import './css/LoginPage.css';
import Modal from 'react-modal';

const LoginPage = () => {
  const { setLog } = useContext(AuthContext);
  const navigate = useNavigate();
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [name, setName] = useState('');
  const videoRef = useRef(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [cameraActive, setCameraActive] = useState(false);

  const handleOpenModal = () => {
    setModalIsOpen(true);
    startCamera();
  };
  
  const handleCloseModal = () => {
    setModalIsOpen(false);
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };
  
  const handleTakePhoto = async () => {
    // await takePicture();
    await faceLogin();
    handleCloseModal();
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        setCameraActive(true);
      }
    } catch (error) {
      console.error('Error accessing the camera:', error);
    }
  };
  const faceLogin = async () => {
    if (videoRef.current) {
        const video = videoRef.current;
        const captureInterval = 1000;
        let imagesToSend = [];

        for (let i = 0; i < 7; i++) {
            await new Promise(resolve => setTimeout(resolve, captureInterval));

            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                if (blob) {
                    imagesToSend.push(blob);
                }
            }, 'image/jpeg'); 
        }

        const userID = 3;
        const username = 'x'; 

        const formData = new FormData();
        formData.append('user_id', userID);
        formData.append('username', username);
        imagesToSend.forEach((imageBlob) => {
            formData.append('list_of_images', imageBlob, 'image.jpg'); 
        });

        try {
            const response = await fetch('http://127.0.0.1:8000/face_recognition/face_auth_recognize', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
              const wait_for_response = await fetch(`http://127.0.0.1:8000/face_recognition/check_recognition_status/${userID}`, {
        method: 'GET'
    });
              const jsonResponse = await wait_for_response.json(); 
              console.log(jsonResponse);
              if (jsonResponse.status === "success") { 
                  setLog();
                  localStorage.setItem('token_payload', jsonResponse.access_token); 
                  navigate('/');
              }
          } else {
              console.error('Error sending data:', response);
          }
        } catch (error) {
            console.error('Error sending data:', error);
        }
    }
};
  const handleLogin = async (e) => {
    e.preventDefault();

    if (cameraActive) {

      try {
        await faceLogin();
      } catch (error) {
        console.error('Error with face login:', error);
      }
    } else {

      axios.post('http://127.0.0.1:8001/login/login', {
        username: username,
        password: password
      })
      .then(response => {
        if (response.status === 200) {
          setLog();
          localStorage.setItem('token_payload', response.data.access_token);
          navigate('/');
        } else {

        }
      })
      .catch(error => {
        if (error.response && error.response.status === 401) {
          setErrorMessage('Invalid username or password. Please try again.');
        } else {
          console.error(error);
        }
      });
    }

    setUsername('');
    setPassword('');
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <div className="form-input">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-input">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="form-buttons">
        <button type="button" onClick={handleOpenModal}>Start Camera</button>
        <Modal
      isOpen={modalIsOpen}
      onRequestClose={handleCloseModal}
      contentLabel="Camera Modal"
      style={{
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)' 
        },
        content: {
          top: '50%',
          left: '50%',
          right: 'auto',
          bottom: 'auto',
          marginRight: '-50%',
          transform: 'translate(-50%, -50%)',
          width: '50%', 
          height: '50%', 
        }
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
  <h2>Enter your name</h2>
  <input
    type="text"
    id = "enter_name"
    value={name}
    onChange={(e) => setName(e.target.value)}
    style={{ margin: '0 auto' }}
  />
</div>
      <video ref={videoRef} autoPlay style={{ width: '30%', height: 'auto' }}></video>
      <button onClick={handleTakePhoto}>Take Photo</button>
      </Modal>
          <button type="submit" className="login-button">Login</button>
          <button type="button" className="login-button">Forgot Password</button>
        </div>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </form>
    </div>
  );
};

export default LoginPage;
