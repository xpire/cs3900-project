import React from "react";
import { Card, CardContent } from "@material-ui/core";

import SortableTable from "../../components/common/SortableTable";
import Page from "../../components/page/Page";

function createData(
  symbol,
  name,
  exchange,
  price,
  shares,
  average,
  total,
  value,
  gain,
  dailyGain,
  totalReturn
) {
  return {
    symbol,
    name,
    exchange,
    price,
    shares,
    average,
    total,
    value,
    gain,
    dailyGain,
    totalReturn,
  };
}

const rows = [
  createData("TLS", "Cupcake", "AAA", 305, 3.7, 67, 4.3, 5, 67, 4.3, 5),
  createData("SVW", "Donut", "AAA", 452, 25.0, 51, 4.9, 6, 67, 4.3, 5),
  createData("TPG", "Eclair", "AAA", 262, 16.0, 24, 6.0, 6, 67, 4.3, 5),
  createData("T", "Frozen yoghurt", "AAA", 159, 35.2, 24, 4.0, 6, 67, 4.3, 5),
  createData("FB", "Gingerbread", "AAA", 356, 16.0, 49, 3.9, 6, 67, 4.3, 5),
  createData("CSCO", "Honeycomb", "AAA", 408, 3.2, 87, 6.5, 6, 67, 4.3, 5),
  createData(
    "VOD",
    "Ice cream sandwich",
    "AAA",
    237,
    109,
    37,
    4.3,
    6,
    67,
    4.3,
    5
  ),
  createData("STJ", "Jelly Bean", "AAA", 375, 0.0, 94, 0.0, 6, 67, 4.3, 5),
  createData("MDC", "KitKat", "AAA", 518, 66, 65, 7.0, 6, 67, 4.3, 5),
];

const headCells = [
  { id: "symbol", numeric: false, disablePadding: false, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "exchange", numeric: false, disablePadding: false, label: "Exchange" },
  { id: "price", numeric: true, disablePadding: false, label: "Price" },
  { id: "shares", numeric: true, disablePadding: false, label: "Shares" },
  {
    id: "average",
    numeric: true,
    disablePadding: false,
    label: "Avg Sale",
  },
  { id: "total", numeric: true, disablePadding: false, label: "Total Sale" },
  { id: "value", numeric: true, disablePadding: false, label: "Value" },

  {
    id: "gain",
    numeric: true,
    disablePadding: false,
    label: "Gain",
    color: true,
  },
  {
    id: "dailyGain",
    numeric: true,
    disablePadding: false,
    label: "Day Gain",
    color: true,
  },
  {
    id: "totalReturn",
    numeric: true,
    disablePadding: false,
    label: "Return",
    color: true,
  },
];

const Portfolio = () => {
  return (
    <Page>
      <Card>
        {/* <CardContent> */}
        <SortableTable data={rows} header={headCells} title="Portfolio" />
        {/* </CardContent> */}
      </Card>
    </Page>
  );
};

export default Portfolio;
