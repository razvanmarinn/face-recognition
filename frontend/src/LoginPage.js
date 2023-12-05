import React, { useState, useRef } from 'react';
import axios from 'axios';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const videoRef = useRef();

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error('Error accessing the camera:', error);
    }
  };

  const takePicture = async () => {
    if (videoRef.current) {
      const video = videoRef.current;
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = canvas.toDataURL('image/png');

      try {
        const response = await axios.post('http://127.0.0.1:8000/face_recognition/recognize', {
          image: imageData,
          username: username,
        });

        console.log('Server Response:', response);
      } catch (error) {
        console.error('Error sending data:', error);
      }
    }
  };

  const handleLogin = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8001/login/login', {
      username: username,
      password: password
    })
    .then(response => {
      if (response.status === 200) {
        window.location.replace('/main');

        localStorage.setItem('token_payload', response.data.access_token);
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

    setUsername('');
    setPassword('');
  };

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && <p>{errorMessage}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <button onClick={startCamera}>Start Camera</button>
          <video ref={videoRef} autoPlay playsInline />
          <button onClick={takePicture}>Take Picture</button>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
