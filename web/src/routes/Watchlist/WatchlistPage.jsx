import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";
import { useSnackbar } from "notistack";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import { format } from "../../utils/formatter";
import useHandleSnack from "../../hooks/useHandleSnack";

const headCells = [
  { id: "symbol", numeric: false, disablePadding: false, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "exchange", numeric: false, disablePadding: false, label: "Exchange" },
  { id: "price", numeric: true, disablePadding: false, label: "Price" },
  { id: "open", numeric: true, disablePadding: false, label: "Open" },
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
    ({ curr_day_close, exchange, name, curr_day_open, symbol }) => {
      return {
        symbol: symbol,
        name: name,
        exchange: exchange,
        price: curr_day_close,
        open: curr_day_open,
        daily: format(curr_day_close - curr_day_open),
        dailyPercentage: format(
          (100 * (curr_day_close - curr_day_open)) / curr_day_open
        ),
      };
    }
  );
  console.log(data);
  const { enqueueSnackbar } = useSnackbar();
  const handleSnack = useHandleSnack();

  return (
    <Page>
      <Card>
        <SortableTable
          data={mappedData}
          header={headCells}
          title="Watch List"
          handleDelete={({ symbol }) => {
            handleSnack(`/watchlist?symbol=${symbol}`, "delete").then(() =>
              setDeleted(deleted + 1)
            );
          }}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
