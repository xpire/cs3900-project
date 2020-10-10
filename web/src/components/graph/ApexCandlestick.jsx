import React from "react";
import Chart from "react-apexcharts";
import { useTheme } from "@material-ui/core";
const Candlestick = ({ data }) => {
  const theme = useTheme();

  return (
    <Chart
      options={{
        theme: {
          mode: theme.palette.type,
        },
        chart: {
          type: "candlestick",
          height: 350,
        },
        xaxis: {
          type: "datetime",
        },
        yaxis: {
          tooltip: {
            enabled: true,
          },
        },
      }}
      series={[{ data: data }]}
      type="candlestick"
    />
  );
};

export default Candlestick;
