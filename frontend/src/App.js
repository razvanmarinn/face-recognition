import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext, AuthProvider } from './AuthContext';
import LoginPage from './LoginPage';
import MainPage from './MainPage';
import Recognize from './Recognize';
import AddFace from './AddFace';
import SharedImagePool from './SharedImagePool.js';
import Profile from './Profile.js'

function App() {
  const { isLoggedIn } = useContext(AuthContext);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={isLoggedIn ? <MainPage /> : <Navigate to="/login" />} />
          <Route path="/recognize" element={isLoggedIn ? <Recognize /> : <Navigate to="/login" />} />
          <Route path="/addface" element={isLoggedIn ? <AddFace /> : <Navigate to="/login" />} />
          <Route path="/shared_image_pool" element={isLoggedIn ? <SharedImagePool /> : <Navigate to="/login" />} />
          <Route path="/profile" element={isLoggedIn ? <Profile /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

function Root() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}

export default Root;