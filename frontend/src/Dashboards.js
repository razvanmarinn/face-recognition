import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,  PieChart, Pie  } from 'recharts';
import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';

import './css//Dashboards.css';

const GenerateDashboards = () => {
  const [dashboardData1, setDashboardData1] = useState([]);
  const [dashboardData2, setDashboardData2] = useState([]); // New state variable for the second dashboard
  const [dashboardData3, setDashboardData3] = useState([]); // New state variable for the third dashboard
  const [dashboardData4, setDashboardData4] = useState([]); 
  const fetchDashboardData1 = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/dashboards/get_succesful_recognitions', {
        method: 'GET'
      });
      const data = await response.json();
      setDashboardData1([{name: 'Recognitions', Successful: data.succesfull_recognitions, Failed: data.failed_recognitions}]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchDashboardData2 = async () => { 
    try {
      const response = await fetch('http://127.0.0.1:8001/user_details/get_number_of_total_users', {
        method: 'GET'
      });
      const data = await response.json();
      setDashboardData2([{name: 'Total Users', total_users: data.total_users}]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };
  const fetchDashboardData3 = async () => { 
    try {
      const response = await fetch('http://127.0.0.1:8000/dashboards/total_sips', {
        method: 'GET'
      });
      const data = await response.json();
      setDashboardData3([{name: 'Total SIPS', Value: data.total_sips}]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchDashboardData4 = async () => { 
    try {
      const response = await fetch('http://127.0.0.1:8003/user_details/get_some_other_data', {
        method: 'GET'
      });
      const data = await response.json();
      setDashboardData4([{name: 'Some Other Data', Value: data.value}]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  useEffect(() => {
    fetchDashboardData1();
    fetchDashboardData2();
    fetchDashboardData3(); 
  }, []);



return (
  <div>
    <Navbar />
    <div className="dashboard">
      <h2>Dashboard 1</h2>
      <BarChart width={500} height={300} data={dashboardData1}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="Successful" fill="#8884d8" />
        <Bar dataKey="Failed" fill="#82ca9d" />
      </BarChart>
      <h2>Dashboard 2</h2>
      <PieChart width={400} height={400}>
        <Pie
          dataKey="total_users"
          isAnimationActive={false}
          data={dashboardData2}
          cx={200}
          cy={200}
          outerRadius={80}
          fill="#8884d8"
          label
        />
        <Tooltip />
      </PieChart>
      <h2>Dashboard 3</h2>
<PieChart width={400} height={400}>
  <Pie
    dataKey="Value" 
    isAnimationActive={false}
    data={dashboardData3}
    cx={200}
    cy={200}
    outerRadius={80}
    fill="#8884d8"
    label
  />
  <Tooltip />
</PieChart>
        </div>
  </div>
);
}

export default GenerateDashboards;