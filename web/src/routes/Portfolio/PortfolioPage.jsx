import React, { useState, useEffect } from "react";
import { Card, CardContent, Tabs, Tab } from "@material-ui/core";

import SortableTable from "../../components/common/SortableTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";

// function createData(
//   symbol,
//   name,
//   exchange,
//   price,
//   shares,
//   average,
//   total,
//   value,
//   gain,
//   dailyGain,
//   totalReturn
// ) {
//   return {
//     symbol,
//     name,
//     exchange,
//     price,
//     shares,
//     average,
//     total,
//     value,
//     gain,
//     dailyGain,
//     totalReturn,
//   };
// }

// const rows = [
//   createData("TLS", "Cupcake", "AAA", 305, 3.7, 67, 4.3, 5, 67, 4.3, 5),
//   createData("SVW", "Donut", "AAA", 452, 25.0, 51, 4.9, 6, 67, 4.3, 5),
//   createData("TPG", "Eclair", "AAA", 262, 16.0, 24, 6.0, 6, 67, 4.3, 5),
//   createData("T", "Frozen yoghurt", "AAA", 159, 35.2, 24, 4.0, 6, 67, 4.3, 5),
//   createData("FB", "Gingerbread", "AAA", 356, 16.0, 49, 3.9, 6, 67, 4.3, 5),
//   createData("CSCO", "Honeycomb", "AAA", 408, 3.2, 87, 6.5, 6, 67, 4.3, 5),
//   createData(
//     "VOD",
//     "Ice cream sandwich",
//     "AAA",
//     237,
//     109,
//     37,
//     4.3,
//     6,
//     67,
//     4.3,
//     5
//   ),
//   createData("STJ", "Jelly Bean", "AAA", 375, 0.0, 94, 0.0, 6, 67, 4.3, 5),
//   createData("MDC", "KitKat", "AAA", 518, 66, 65, 7.0, 6, 67, 4.3, 5),
// ];

const headCells = [
  { id: "symbol", numeric: false, disablePadding: false, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "price", numeric: false, disablePadding: false, label: "Price" },
  {
    id: "previous_price",
    numeric: true,
    disablePadding: false,
    label: "Previous Price",
  },
  { id: "owned", numeric: true, disablePadding: false, label: "Owned" },
  {
    id: "average_paid",
    numeric: true,
    disablePadding: false,
    label: "Avg Paid",
  },
  {
    id: "total_paid",
    numeric: true,
    disablePadding: false,
    label: "Total Paid",
  },
  { id: "value", numeric: true, disablePadding: false, label: "Value" },

  {
    id: "gain",
    numeric: true,
    disablePadding: false,
    label: "Gain",
    color: true,
  },
  {
    id: "day_gain",
    numeric: true,
    disablePadding: false,
    label: "Day Gain",
    color: true,
  },
  {
    id: "return",
    numeric: true,
    disablePadding: false,
    label: "Return",
    color: true,
  },
];

const Portfolio = () => {
  const [long, setLong] = useState([]);
  const [short, setShort] = useState([]);
  const [tab, setTab] = useState(0);
  useEffect(() => {
    axios
      .get("/portfolio")
      .then((response) => {
        console.log({ response });
        setLong(response.data.long);
        setShort(response.data.short);
      })
      .catch((err) => console.log(err));
  }, []);
  return (
    <Page>
      <Card>
        <Tabs
          value={tab}
          onChange={(_event, newValue) => {
            console.log("setting value to", newValue);
            setTab(newValue);
          }}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Longs" />
          <Tab label="Shorts" />
        </Tabs>
        {tab === 0 ? (
          <SortableTable data={long} header={headCells} title="Portfolio" />
        ) : (
          <SortableTable data={short} header={headCells} title="Portfolio" />
        )}
      </Card>
    </Page>
  );
};

export default Portfolio;
