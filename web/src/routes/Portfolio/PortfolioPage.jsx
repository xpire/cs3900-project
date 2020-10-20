import React from "react";
import { Card } from "@material-ui/core";

import SortableTable from "../../components/common/SortableTable";
import Page from "../../components/page/Page";

function createData(
  symbol,
  name,
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
  createData("TLS", "Cupcake", 305, 3.7, 67, 4.3, 5, 67, 4.3, 5),
  createData("SVW", "Donut", 452, 25.0, 51, 4.9, 6, 67, 4.3, 5),
  createData("TPG", "Eclair", 262, 16.0, 24, 6.0, 6, 67, 4.3, 5),
  createData("T", "Frozen yoghurt", 159, 35.2, 24, 4.0, 6, 67, 4.3, 5),
  createData("FB", "Gingerbread", 356, 16.0, 49, 3.9, 6, 67, 4.3, 5),
  createData("CSCO", "Honeycomb", 408, 3.2, 87, 6.5, 6, 67, 4.3, 5),
  createData("VOD", "Ice cream sandwich", 237, 109, 37, 4.3, 6, 67, 4.3, 5),
  createData("STJ", "Jelly Bean", 375, 0.0, 94, 0.0, 6, 67, 4.3, 5),
  createData("MDC", "KitKat", 518, 66, 65, 7.0, 6, 67, 4.3, 5),
];

const headCells = [
  { id: "symbol", numeric: false, disablePadding: true, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "price", numeric: true, disablePadding: false, label: "Price" },
  { id: "shares", numeric: true, disablePadding: false, label: "Shares" },
  {
    id: "average",
    numeric: true,
    disablePadding: false,
    label: "Average Sale $",
  },
  { id: "total", numeric: true, disablePadding: false, label: "Total Sale $" },
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
        <SortableTable data={rows} header={headCells} title="Portfolio" />
      </Card>
    </Page>
  );
};

export default Portfolio;
