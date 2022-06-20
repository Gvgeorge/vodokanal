import React, { useEffect, useState } from "react";
import axios from "axios";


const Table = () => {
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

    return (
        <div className="orders">
                <div className="order-table">
                    <table>
                        <thead>
                            <tr>
                                <th>№</th><th>заказ №</th><th>стоимость, $</th><th>срок поставки</th>
                            </tr>
                        </thead>
                        <tbody>
                        {orders.map((order, index) =>
                        <tr key={index}>
                            <td>{order.row_id}</td>
                            <td>{order.order_id}</td>
                            <td>{order.amount_usd /10000}</td>
                            <td>{new Date(order.date).toLocaleDateString('ru-RU')}</td>

                        </tr>)}
                        </tbody>
                    </table>
                </div>
        </div>)
}

export default Table;