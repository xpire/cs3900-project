import React from "react";
import Chart from "react-apexcharts";
import { useTheme } from "@material-ui/core";
const Cumulative = ({ data }) => {
  const theme = useTheme();

  return (
    <Chart
      options={{
        theme: {
          mode: theme.palette.type,
        },
        chart: {
          type: "area",
          height: 350,
          zoom: {
            autoScaleYaxis: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        markers: {
          size: 0,
          style: "hollow",
        },
        xaxis: {
          type: "datetime",
        },
        yaxis: {
          tooltip: {
            enabled: true,
          },
          decimalsInFloat: 0,
        },
      }}
      series={[{ data: data }]}
      type="area"
    />
  );
};

export default Cumulative;
