import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import 'chart.js/auto';
import './clientmanagement.css';
//updated


const ClientManagement = () => {
  const [data, setData] = useState([]);
  const [clientInput, setClientInput] = useState(true);
  const [ca, setCa] = useState(false);
  const [dbDisplay, setDbDisplay] = useState(false);
  const rows = [];
  
  
  const [activeButtonId, setActiveButtonId] = useState('');

  //set the form writing stuff

  const [form, setForm] = useState({
    collection: 'FSE-CLIENTS',
    document: '',
    fields: {
      FirstName: '',
      LastName: '',
      Age: '',
      Objective: '',
      TimeHorizon: '',
      Date: new Date().toISOString().split('T')[0]
    }
  });

  useEffect(() => {
    fetchData();
  }, []);


  //

  const fetchData = async () => {
    try {
      const response = await axios.post('http://localhost:4001/read', {
        collection: "FSE-CLIENTS"
      });
  
      // Check if 'FSE-CLIENTS' and 'documents' exist
      if (response.data['FSE-CLIENTS'] && response.data['FSE-CLIENTS'].documents) {
        const clientsData = response.data['FSE-CLIENTS'].documents;
        // Extract data from each document's 'fields'
        const formattedData = Object.keys(clientsData).map(key => ({
          document: key,
          ...clientsData[key].fields // Accessing 'fields' for each document
        }));
  
        setData(formattedData);
      } else {
        console.error('No data found for FSE-CLIENTS');
        setData([]);  // Handle cases where there are no documents
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  
  
  //handle inputs

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    if (name in form.fields) {
      setForm((prevForm) => ({
        ...prevForm,
        fields: {
          ...prevForm.fields,
          [name]: value
        }
      }));
    } else {
      setForm((prevForm) => ({
        ...prevForm,
        [name]: value
      }));
    }
  };

  //handle form submits

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:4002/write', form);
      fetchData();
    } catch (error) {
      console.error('Error writing data:', error);
    }
  };

  //handle button clicks

  const handleButtonClick = (buttonId) => {
    setActiveButtonId(buttonId);

    if (buttonId === 'ci') {
      setClientInput(true);
      setDbDisplay(false);
      setCa(false);
      document.getElementById("ci").style.color = "white"
      document.getElementById("di").style.color = "black"
      document.getElementById("cd").style.color = "black"
    }

    if (buttonId === 'di') {
      setClientInput(false);
      setDbDisplay(true);
      setCa(false);
      document.getElementById("ci").style.color = "black"
      document.getElementById("di").style.color = "white"
      document.getElementById("cd").style.color = "black"
    }

    if (buttonId === 'cd') {
      setClientInput(false);
      setDbDisplay(false);
      setCa(true);
      document.getElementById("ci").style.color = "black"
      document.getElementById("di").style.color = "black"
      document.getElementById("cd").style.color = "white"
    }
  };
  //extract objectives for accounts for use in charts
  const getObjectiveCounts = () => {
    const objectiveCounts = {};
    data.forEach((doc) => {
      const objective = doc.Objective;
      if (objective) {
        if (objectiveCounts[objective]) {
          objectiveCounts[objective]++;
        } else {
          objectiveCounts[objective] = 1;
        }
      }
    });
    return objectiveCounts;
  };

  //get yearly counts for use in charts

  const getYearlyCounts = () => {
    const yearlyCounts = {};
    data.forEach((doc) => {
      const year = new Date(doc.Date).getFullYear();
      if (year) {
        if (yearlyCounts[year]) {
          yearlyCounts[year]++;
        } else {
          yearlyCounts[year] = 1;
        }
      }
    });
    return yearlyCounts;
  };

  const objectiveCounts = getObjectiveCounts();
  const yearlyCounts = getYearlyCounts();

  //pie chart dynamic production

  const pieData = {
    labels: Object.keys(objectiveCounts),
    datasets: [
      {
        data: Object.values(objectiveCounts),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          'yellow',
          'green',
          'blue'
        ]
      }
    ]
  };

  //bar chart dynamic production

  const barData = {
    labels: Object.keys(yearlyCounts),
    datasets: [
      {
        label: 'Clients per Year',
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          'yellow',
          'green',
          'blue'
        ],
        borderColor: 'rgba(0,0,0,1)',
        borderWidth: 2,
        data: Object.values(yearlyCounts)
      }
    ]
  };
  


  return (
    <div style={{ marginLeft: '20%', width: '80%', backgroundColor: '#FFFDD0' }}>
      <div style={{ marginTop: '0.5%' }}>
        <button id="ci" onClick={() => handleButtonClick('ci')} style={{ backgroundColor: activeButtonId === 'ci' ? 'maroon' : 'transparent', borderRadius:'10px' }}>Client Details</button>
        <button id="di" onClick={() => handleButtonClick('di')} style={{ marginLeft: '2%', marginRight: '2%', backgroundColor: activeButtonId === 'di' ? 'maroon' : 'transparent', borderRadius:'10px' }}>Client Database</button>
        <button id="cd" onClick={() => handleButtonClick('cd')} style={{ width: '130px', backgroundColor: activeButtonId === 'cd' ? 'maroon' : 'transparent' , borderRadius:'10px'}}>At a Glance</button>
      </div>
      {clientInput && (
        <div id="client-input">
          <br/> <br/>
          
          <form onSubmit={handleSubmit} id="si-form" style={{ zoom: '93%' }}>
            <input
              type="text"
              name="collection"
              value={form.collection}
              onChange={handleInputChange}
              placeholder="Main Collection"
              style={{ display: 'none' }}
            />
            <input
              type="text"
              name="fields.Date"
              value={form.fields.Date}
              onChange={handleInputChange}
              style={{ display: 'none' }}
              
            />
            <label>ID: </label>
            <input
              type="text"
              name="document"
              value={form.document}
              onChange={handleInputChange}
              placeholder="ID"
            />
            <label>First Name: </label>
            <input
              type="text"
              name="FirstName"
              value={form.fields.FirstName}
              onChange={handleInputChange}
              placeholder="First Name"
            />
            <label>Last Name: </label>
            <input
              type="text"
              name="LastName"
              value={form.fields.LastName}
              onChange={handleInputChange}
              placeholder="Last Name"
            />
            <label>Age: </label>
            <input
              type="text"
              name="Age"
              value={form.fields.Age}
              onChange={handleInputChange}
              placeholder="Age"
            />
            <label>Objective: </label>
            <input
              type="text"
              name="Objective"
              value={form.fields.Objective}
              onChange={handleInputChange}
              placeholder="Objective"
            />
            <label>Time Horizon (Months):</label>
            <input
              type="text"
              name="TimeHorizon"
              value={form.fields.TimeHorizon}
              onChange={handleInputChange}
              placeholder="Time Horizon"
            />
            <button type="submit">Submit</button>
          </form>
        </div>
      )}
      {dbDisplay &&(
        <div id="client-database">
          <h1 style={{ marginTop: '1%', marginBottom:'1%' }}>Client Database</h1>
          <table border="1" style={{ width: '95%' }}>
  <thead>
    <tr>
      <th>First Name</th>
      <th>Last Name</th>
      <th>Age</th>
      <th>Objective</th>
      <th>Time Horizon(Months)</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    {data.map((doc) => (
      <tr key={doc.document}>
        <td>{doc.FirstName || 'N/A'}</td>
        <td>{doc.LastName || 'N/A'}</td>
        <td>{doc.Age || 'N/A'}</td>
        <td>{doc.Objective || 'N/A'}</td>
        <td>{doc.TimeHorizon || 'N/A'}</td>
        <td>{doc.Date || 'N/A'}</td>
      </tr>
    ))}
  </tbody>
</table>

        </div>
      )}
      {ca && (

        <div>
          <h1>At A Glance</h1>
 
        
        <div style = {{display:"flex", width:'100%'}}>
          <br/>
          <br/>
          

          <div className="chart-container" style = {{height:'71vh', width:"48%", border:"solid black 1px", paddingTop:'5%', marginLeft:"2%", backgroundColor:"transparent"}}>
            <h1>Client Growth Over Years</h1>
            <Bar data={barData} />
          </div>
          <div  className="chart-container" style = {{height:'80vh', width:"40%", border:"solid black 1px", marginLeft:"2%" , backgroundColor:"transparent"}}>
            <h3>Objectives Share</h3>
            <Pie data={pieData} />
          </div>

        </div>
        </div>
      )}
    </div>
  );
};

export default ClientManagement;
