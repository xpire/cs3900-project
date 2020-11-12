import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import { format } from "../../utils/formatter";
import useHandleSnack from "../../hooks/useHandleSnack";
import axios from "../../utils/api";

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
    formatType: tableTypes.PERCENTAGE,
    disablePadding: false,
    label: "% Day Change",
    color: true,
  },
];

const Watchlist = () => {
  const [deleted, setDeleted] = useState(0);
  const [data] = useRealTimeStockData("/watchlist", [deleted], []);
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

  return (
    <Page>
      <Card>
        <SortableTable
          data={mappedData}
          header={headCells}
          title="Watch List"
          handleDelete={({ symbol }) => {
            axios
              .delete(`/watchlist?symbol=${symbol}`)
              .then(() => setDeleted(deleted + 1));
          }}
          handleRefresh={() => setDeleted(deleted + 1)}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
