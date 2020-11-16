import React, { useState, useEffect } from "react";
import { Card, Tabs, Tab } from "@material-ui/core";

import { tableTypes } from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";

const columns = (negative = false) => [
  {
    field: "symbol",
    title: (
      <RenderItem title="Symbol" subtitle="Shares" alignItems="flex-start" />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.owned}
        subtitleType={tableTypes.SHARES}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "price",
    title: <RenderItem title="Price" subtitle="Chg/Chg%" />,
    render: (rowData) => {
      const change = rowData.price - rowData.previous_price;
      const percentChange = (change / rowData.previous_price) * 100;
      return (
        <RenderItem
          title={rowData.price}
          titleType={tableTypes.CURRENCY}
          subtitle={change}
          subtitleColor={true}
          subtitleType={tableTypes.CURRENCY}
          subtitleNegative={negative}
          subsubtitle={percentChange}
          subsubtitleType={tableTypes.PERCENTAGE}
          subsubtitleColor={true}
          subsubtitleNegative={negative}
        />
      );
    },
    align: "right",
  },
  {
    field: "value",
    title: <RenderItem title="Value" subtitle="Gain/Loss" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.value}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.profit}
        subtitleColor={true}
        subtitleType={tableTypes.CURRENCY}
        subtitleNegative={negative}
        subsubtitle={rowData.total_return}
        subsubtitleType={tableTypes.PERCENTAGE}
        subsubtitleColor={true}
        subsubtitleNegative={negative}
      />
    ),
    align: "right",
  },
  {
    field: "day_profit",
    title: <RenderItem title="Daily Profit" subtitle="Daily Return" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.day_profit}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.day_return}
        subtitleColor={true}
        subtitleType={tableTypes.PERCENTAGE}
        subtitleNegative={negative}
      />
    ),
    align: "right",
  },
  {
    field: "average_paid",
    title: <RenderItem title="Avg Paid" subtitle="Total Paid" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.average_paid}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.total_paid}
        subtitleType={tableTypes.CURRENCY}
      />
    ),
    align: "right",
  },
];

const Portfolio = () => {
  const [long, setLong] = useState([]);
  const [short, setShort] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [tab, setTab] = useState(0);

  const refreshTable = () => {
    setIsLoading(true);
    axios
      .get("/portfolio")
      .then((response) => {
        setLong(response.data.long);
        setShort(response.data.short);
        setIsLoading(false);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    refreshTable();
  }, []);

  const handleRefresh = () => {
    refreshTable();
  };

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
        <SortableStockTable
          title="Portfolio"
          columns={columns(tab === 1)}
          data={tab === 0 ? long : short}
          isLoading={isLoading}
          handleRefresh={handleRefresh}
        />
        {/* {tab === 0 ? (
          <SortableStockTable
            title="Portfolio"
            columns={columns}
            data={long}
            isLoading={isLoading}
            handleRefresh={handleRefresh}
          />
        ) : (
          <SortableStockTable
            title="Portfolio"
            columns={columns}
            data={short}
            isLoading={isLoading}
            handleRefresh={handleRefresh}
          />
        )} */}
      </Card>
    </Page>
  );
};

export default Portfolio;
