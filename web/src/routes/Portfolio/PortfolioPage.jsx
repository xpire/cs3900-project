import React, { useState, useEffect } from "react";
import { Card, CardContent, Tabs, Tab } from "@material-ui/core";

import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import Page from "../../components/page/Page";
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
    id: "price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Price",
  },
  {
    id: "previous_price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Previous Price",
  },
  {
    id: "owned",
    formatType: tableTypes.NUMBER,
    disablePadding: false,
    label: "Owned",
  },
  {
    id: "average_paid",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Avg Paid",
  },
  {
    id: "total_paid",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Total Paid",
  },
  {
    id: "value",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Value",
  },

  {
    id: "profit",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Gain",
    color: true,
  },
  {
    id: "day_profit",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Day Profit",
    color: true,
  },
  {
    id: "total_return",
    formatType: tableTypes.CURRENCY,
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
