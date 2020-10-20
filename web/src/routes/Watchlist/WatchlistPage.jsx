import React from "react";
import { Typography, Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";

function createData(symbol, name, price, open, close, daily, dailyPercentage) {
  return { symbol, name, price, open, close, daily, dailyPercentage };
}

const rows = [
  createData("TLS", "Cupcake", 305, 3.7, 67, 4.3, 5),
  createData("SVW", "Donut", 452, 25.0, 51, 4.9, 6),
  createData("TPG", "Eclair", 262, 16.0, 24, 6.0, 6),
  createData("T", "Frozen yoghurt", 159, 35.2, 24, 4.0, 6),
  createData("FB", "Gingerbread", 356, 16.0, 49, 3.9, 6),
  createData("CSCO", "Honeycomb", 408, 3.2, 87, 6.5, 6),
  createData("VOD", "Ice cream sandwich", 237, 109, 37, 4.3, 6),
  createData("STJ", "Jelly Bean", 375, 0.0, 94, 0.0, 6),
  createData("MDC", "KitKat", 518, 66, 65, 7.0, 6),
];

const headCells = [
  { id: "symbol", numeric: false, disablePadding: true, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "price", numeric: true, disablePadding: false, label: "Price" },
  { id: "open", numeric: true, disablePadding: false, label: "Open" },
  { id: "close", numeric: true, disablePadding: false, label: "Close" },
  { id: "daily", numeric: true, disablePadding: false, label: "Day Change" },
  {
    id: "dailyPercentage",
    numeric: true,
    disablePadding: false,
    label: "% Day Change",
  },
];

const Watchlist = () => {
  return (
    <Page>
      <Card>
        <SortableTable data={rows} header={headCells} />
      </Card>
    </Page>
  );
};

export default Watchlist;
