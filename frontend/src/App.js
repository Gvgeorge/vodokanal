import './App.css';
import Header from './components/header';
import Table from './components/table';
import Total from './components/total';
import OrdersChart from './components/ordersChart';



function App() {
  return (
    <div className="App">
      <Header />
      <div className='container'>
        <Table />
        <Total />

      </div>
      <OrdersChart />
    </div>
  );
}

export default App;
