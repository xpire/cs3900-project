import React, { useContext, useState } from "react";
import { Typography, AppBar, Tab, Tabs, Grid, Box } from "@material-ui/core";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard, ColoredText } from "../../components/common/styled";
import CardGrid from "../../components/common/CardGrid";
import ApexCandlestick from "../../components/graph/ApexCandlestick";

import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call
import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

const stockData = data.data; //.slice(0, 30);

const parsedApexData = TimeSeriesData.AAPL.values
  .map(({ datetime, open, close, high, low }) => {
    return { x: new Date(datetime), y: [open, high, low, close] };
  })
  .slice(0, 365);

const StatCard = ({ name, value, stat, today }) => {
  return (
    <StandardCard style={{ height: "150px" }}>
      {/* TODO: make this not hardcoded somehow */}
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item xs={12} container>
          <Typography variant="button">{name}</Typography>
        </Grid>
        <Grid item container alignItems="flex-end" spacing={1}>
          <Grid item>
            <Typography variant="h4">{value}</Typography>
          </Grid>
          {stat && (
            <Grid item>
              <ColoredText color={stat > 0 ? "green" : "red"} variant="h5">
                ({stat})
              </ColoredText>
            </Grid>
          )}
        </Grid>
        {today && (
          <>
            <Grid item xs={12}>
              <Typography variant="subtitle2">Today:</Typography>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="caption">{today}</Typography>
            </Grid>
          </>
        )}
      </Grid>
    </StandardCard>
  );
};

const StatisticsData = [
  { name: "Portfolio Value", value: 21123.33, stat: 5.3, today: -1.4 },
  { name: "Net Value", value: 26992.23, stat: 23, today: 2 },
  { name: "Profit", value: 1992.23, stat: 4.3, today: 10.4 },
  { name: "Available Balance", value: 5001.22 },
];

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      // id={`simple-tabpanel-${index}`}
      // aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
};

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [value, setValue] = useState(0);
  return (
    <Page>
      <div style={{ padding: "12px" }}>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
          spacing={1}
        >
          {StatisticsData.map((data) => (
            <Grid item md={3} sm={6} xs={12}>
              <StatCard {...data} />
            </Grid>
          ))}
          <Grid xs={12}>
            <StandardCard>
              <ApexCandlestick data={parsedApexData} />
            </StandardCard>
          </Grid>
          <Grid xs={12}>
            <StandardCard>
              <Tabs
                value={value}
                onChange={(_event, newValue) => setValue(newValue)}
                indicatorColor="primary"
                textColor="primary"
                variant="fullWidth"
              >
                <Tab label="Longs" />
                <Tab label="Shorts" />
                <Tab label="Watchlist" />
              </Tabs>
            </StandardCard>
            <TabPanel value={value} index={0}>
              <CardGrid data={stockData.slice(0, 30)} />
            </TabPanel>
            <TabPanel value={value} index={1}>
              <CardGrid data={stockData.slice(15, 30)} />
            </TabPanel>
            <TabPanel value={value} index={2}>
              <CardGrid data={stockData.slice(30, 40)} />
            </TabPanel>
          </Grid>
        </Grid>
      </div>
    </Page>
  );
};

export default Dashboard;
