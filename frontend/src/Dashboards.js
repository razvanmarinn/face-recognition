import React, { useState, useEffect } from 'react';
import './css/Dashboards.css';
import Navbar from './Navbar';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const GenerateDashboards = () => {
  const [dashboardData, setDashboardData] = useState([]);

  const fetchDashboardData = async () => {
    try {
      const jwt = localStorage.getItem('token_payload');
      const response = await fetch('http://127.0.0.1:8000/dashboards/get_succesful_recognitions', {
        method: 'GET'
      });
      const data = await response.json();
      setDashboardData([{name: 'Recognitions', Successful: data.succesfull_recognitions, Failed: data.failed_recognitions}]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <div>
      <Navbar />
      <div className="dashboard">
        <BarChart width={500} height={300} data={dashboardData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="Successful" fill="#8884d8" />
          <Bar dataKey="Failed" fill="#82ca9d" />
        </BarChart>
      </div>
    </div>
  );
}

export default GenerateDashboards;