import React, { useEffect, useState } from "react";
import axios from "axios";


const Total = () => {
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
      }

    const orderSum = orders.reduce((partialSum, a) => partialSum + a['amount_usd'], 0) / 10000;
    return (<div className="total">
        <div className="total-title">
            Total
        </div>
        <h1>{orderSum}</h1>
    </div>)
}
export default Total;
