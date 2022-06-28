import { Line } from "react-chartjs-2";
import Chart from 'chart.js/auto';
import {CategoryScale} from 'chart.js'; 

Chart.register(CategoryScale);


const OrdersChart = ({orders}) => {
    let sortedOrders = orders.sort(function (a, b) {
        return (new Date(a['date']) - new Date(b['date']))}
        )

        const lineChartData = {
            labels: sortedOrders.map(order => order['date']),
            datasets: [
              {
                data: sortedOrders.map(order => order['amount_usd']/10000),
                label: orders,
                borderColor: "#3333ff",
                fill: true,
                lineTension: 0
              },
            ]
          };
        
          return (
            <div className="chart">
              <Line
                type="line"
                width={160}
                height={60}
                options={{
                  title: {
                    display: false,
                    text: "Recent orders",
                    fontSize: 20
                  },
                  legend: {
                    display: false, //Is the legend shown?
                    position: "top" //Position of the legend.
                  }
                }}
                data={lineChartData}
              />
          </div>
          );
        };


export default OrdersChart;