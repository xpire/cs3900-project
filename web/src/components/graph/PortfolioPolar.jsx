import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { useTheme } from "@material-ui/core";

const PortfolioPolar = ({ data }) => {
  const theme = useTheme();

  return (
    <Chart
      options={{
        chart: {
          width: 1000,
          type: "pie",
          animations: {
            enabled: false,
          },
        },
        theme: {
          mode: theme.palette.type,
        },
        // stroke: {
        //   colors: ["#fff"],
        // },
        yaxis: {
          // show: false,
          // floating: true,
          forceNiceScale: true,
          // tickamount: 6,
          // min: 0,
          // max: 100,
          // labels: {
          // // tickAmount: 5,
          // // show: false
          //   formatter: function(val, index) {
          //     return val.toFixed(0);
          //   }
          // }
        },
        fill: {
          opacity: 0.8,
        },
        tooltip: {
          // x: {
          //   show: true,
          //   format: 'dd MMM',
          //   formatter: (val, index) => {return val.toFixed(2)},
          // },
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],

        // labels: ["Nothing"]
        labels: data.length == 0 ? ["No values"] : data.map((item) => item[0]),
      }}
      series={data.length == 0 ? [0] : data.map((item) => item[1])}
      // series={[50]}
      type="pie"
    />
  );
};

export default PortfolioPolar;
