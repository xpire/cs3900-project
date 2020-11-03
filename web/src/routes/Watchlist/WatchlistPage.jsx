import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import { format } from "../../utils/formatter";
import useHandleSnack from "../../hooks/useHandleSnack";

const headCells = [
  {
    id: "symbol",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Symbol",
  },
  {
    id: "name",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Name",
  },
  {
    id: "exchange",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Exchange",
  },
  {
    id: "price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Price",
  },
  {
    id: "open",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Open",
  },
  {
    id: "daily",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Day Change",
    color: true,
  },
  {
    id: "dailyPercentage",
    formatType: tableTypes.FLOAT,
    disablePadding: false,
    label: "% Day Change",
    color: true,
  },
];

const Watchlist = () => {
  // const [data, setData] = useState([]);
  const [deleted, setDeleted] = useState(0);
  const [data] = useRealTimeStockData("/watchlist", [deleted], []);
  const mappedData = data.map(
    ({ curr_close_price, exchange, name, prev_close_price, symbol }) => {
      return {
        symbol: symbol,
        name: name,
        exchange: exchange,
        price: curr_close_price,
        open: prev_close_price,
        daily: format(curr_close_price - prev_close_price),
        dailyPercentage: format(
          (100 * (curr_close_price - prev_close_price)) / prev_close_price
        ),
      };
    }
  );
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
          handleRefresh={() => setDeleted(deleted + 1)}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
