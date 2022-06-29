const Table = ({ orders }) => {
  return (
    <div className="orders">
      <div className="order-table">
        <table>
          <thead>
            <tr>
              <th>№</th>
              <th>заказ №</th>
              <th>стоимость, $</th>
              <th>срок поставки</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order, index) => (
              <tr key={index}>
                <td>{order.row_id}</td>
                <td>{order.order_id}</td>
                <td>{order.amount_usd / 10000}</td>
                <td>{new Date(order.date).toLocaleDateString("ru-RU")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Table;
