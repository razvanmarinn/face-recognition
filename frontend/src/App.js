// App.js
import React from 'react';
import './App.css';
import LoginForm from './LoginPage';
import MainPage from './MainPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/main" element={<MainPage />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App;
