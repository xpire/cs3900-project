import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";
import axios from "../../utils/api";
import { useSnackbar } from "notistack";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";

// function createData(symbol, name, price, open, close, daily, dailyPercentage) {
//   return { symbol, name, price, open, close, daily, dailyPercentage };
// }

// const rows = [
//   createData("TLS", "Cupcake", 305, 3.7, 67, 4.3, 5),
//   createData("SVW", "Donut", 452, 25.0, 51, 4.9, 6),
//   createData("TPG", "Eclair", 262, 16.0, 24, 6.0, 6),
//   createData("T", "Frozen yoghurt", 159, 35.2, 24, 4.0, 6),
//   createData("FB", "Gingerbread", 356, 16.0, 49, 3.9, 6),
//   createData("CSCO", "Honeycomb", 408, 3.2, 87, 6.5, 6),
//   createData("VOD", "Ice cream sandwich", 237, 109, 37, 4.3, 6),
//   createData("STJ", "Jelly Bean", 375, 0.0, 94, 0.0, 6),
//   createData("MDC", "KitKat", 518, 66, 65, 7.0, 6),
// ];

const headCells = [
  { id: "symbol", numeric: false, disablePadding: false, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "exchange", numeric: false, disablePadding: false, label: "Exchange" },
  { id: "price", numeric: true, disablePadding: false, label: "Price" },
  { id: "open", numeric: true, disablePadding: false, label: "Open" },
  { id: "close", numeric: true, disablePadding: false, label: "Close" },
  {
    id: "daily",
    numeric: true,
    disablePadding: false,
    label: "Day Change",
    color: true,
  },
  {
    id: "dailyPercentage",
    numeric: true,
    disablePadding: false,
    label: "% Day Change",
    color: true,
  },
];

const Watchlist = () => {
  // const [data, setData] = useState([]);
  const [deleted, setDeleted] = useState(0);
  const [data, loading] = useRealTimeStockData("/watchlist", [deleted], []);
  const mappedData = data.map(
    ({ curr_close_price, exchange, name, prev_close_price, symbol }) => {
      return {
        symbol: symbol,
        name: name,
        exchange: exchange,
        price: curr_close_price,
        open: 1111,
        close: prev_close_price,
        daily: (curr_close_price - prev_close_price).toFixed(2),
        dailyPercentage: (
          (100 * (curr_close_price - prev_close_price)) /
          prev_close_price
        ).toFixed(2),
      };
    }
  );
  console.log(data);
  const { enqueueSnackbar } = useSnackbar();
  // useEffect(() => {
  //   axios
  //     .get("/watchlist")
  //     .then((response) => {
  //       setData(response.data);
  //     })
  //     .catch((err) => console.log(err));
  // }, [deleted]);
  return (
    <Page>
      <Card>
        {/* <CardContent> */}
        <SortableTable
          data={mappedData}
          header={headCells}
          title="Watch List"
          handleDelete={(symbol) => {
            axios
              .delete(`/watchlist?symbol=${symbol}`)
              .then((response) => {
                console.log({ response });
                response.data?.result === "success"
                  ? enqueueSnackbar(
                      `${response.data.result}! ${symbol} deleted from watchlist`,
                      {
                        variant: "Success",
                      }
                    )
                  : enqueueSnackbar(`${response.data.result}`, {
                      variant: "Warning",
                    });
                setDeleted(deleted + 1);
                console.log({ response });
                console.log(response.data.result === "success");
              })
              .catch((err) =>
                enqueueSnackbar(`${err}`, {
                  variant: "Error",
                })
              );
          }}
        />
        {/* </CardContent> */}
      </Card>
    </Page>
  );
};

export default Watchlist;
