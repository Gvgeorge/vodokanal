const Total = ({ orders }) => {
  const orderSum =
    orders.reduce((partialSum, a) => partialSum + a["amount_usd"], 0) / 10000;

  return (
    <div className="total">
      <div className="total-title">Total</div>
      <h1>{orderSum}</h1>
    </div>
  );
};
export default Total;
