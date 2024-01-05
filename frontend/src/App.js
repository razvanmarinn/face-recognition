import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext, AuthProvider } from './AuthContext';
import LoginPage from './LoginPage';
import MainPage from './MainPage';
import Recognize from './Recognize';

function App() {
  const { isLoggedIn } = useContext(AuthContext);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/home" element={isLoggedIn ? <MainPage /> : <Navigate to="/login" />} />
          <Route path="/recognize" element={isLoggedIn ? <Recognize /> : <Navigate to="/login" />} />
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