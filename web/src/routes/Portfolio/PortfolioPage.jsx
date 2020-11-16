import React, { useState, useEffect } from "react";
import { Card, Tabs, Tab } from "@material-ui/core";
import { Typography, Grid } from "@material-ui/core";

import SortableStockTable, {
  tableTypes,
  RenderItem,
} from "../../components/common/SortableStockTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";
import PortfolioPolar from "../../components/graph/PortfolioPolar";
import { useSelector, useDispatch } from "react-redux";

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
  const [isLoading, setIsLoading] = useState(false);
  const [tab, setTab] = useState(0);

  // PORTFOLIO DATA
  const { long, short } = useSelector((state) => state.user.portfolio);

  const positionsToData = (positions) => {
    return positions.map((item) => [
      `${item.symbol}: ${item.owned}`,
      Number(item.total_paid.toFixed(2)),
    ]);
  };
  const longData = positionsToData(long);
  const shortData = positionsToData(short);

  return (
    <Page>
      <Card>
        <Grid item container direction="row">
          <Grid item xs={12} sm={6}>
            <Typography variant="h4" style={{ padding: "10px" }}>
              Long
            </Typography>
            <Grid container style={{ maxHeight: "300px", padding: "10px" }}>
              <PortfolioPolar data={longData} />
            </Grid>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="h4" style={{ padding: "10px" }}>
              Short
            </Typography>
            <Grid container style={{ maxHeight: "300px", padding: "10px" }}>
              <PortfolioPolar data={shortData} />
            </Grid>
          </Grid>
        </Grid>
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
        />
      </Card>
    </Page>
  );
};

export default Portfolio;
