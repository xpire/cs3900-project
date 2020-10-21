import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";
import axios from "../../utils/api";
import { useSnackbar } from "notistack";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";

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
  return (
    <Page>
      <Card>
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
      </Card>
    </Page>
  );
};

export default Watchlist;
