import './App.css';
import Header from './components/header';
import Total from './components/total';
import Table from './components/table';
import OrdersChart from './components/ordersChart';
import React, { useEffect, useState } from "react";
import axios from "axios";



function App() {

      let [orders, setOrders] = useState([]);
        
      useEffect(() => {getOrders()}, [])

      let getOrders = () => {

          axios.get('http://localhost:5555/')
          .then(function (response) {
              let data = response.data['orders'];
              setOrders(data);
          })
          .catch(function (error) {
              console.log(error);
          })
  };

  setInterval(getOrders, 30000)
  return (

    <div className="App">
      <Header />
      <div className='container'>
        <Total orders={orders} />
        <Table orders={orders} />
      </div>
      <OrdersChart orders={orders} />
    </div>
  );
}

export default App;
