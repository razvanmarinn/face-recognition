import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8001/login/login', {
      username: username,
      password: password
    })
    .then(response => {
      if (response.status === 200) {
        window.location.replace('/main');
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
