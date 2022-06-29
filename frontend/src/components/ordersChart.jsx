import { Line } from "react-chartjs-2";
import Chart from 'chart.js/auto';
import {CategoryScale, Title, Legend} from 'chart.js'; 

Chart.register(CategoryScale, Title, Legend);


const OrdersChart = ({orders}) => {
    let sortedOrders = orders.sort(function (a, b) {
        return (new Date(a['date']) - new Date(b['date']))}
        )
        const lineChartData = {
            labels: sortedOrders.map(order => order['date']),
            datasets: [
              {
                data: sortedOrders.map(order => order['amount_usd']/10000),
                label: 'Recent orders',
                borderColor: "#3333ff",
                fill: true,
                lineTension: 0,
              },
            ]

          };
          return (
            <div className="chart">
              <Line
                type="line"
                width={160}
                height={60}
                data={lineChartData}
              />
          </div>
          );
        };


export default OrdersChart;