import React, { useContext, useState, useEffect } from "react";
import { Typography, Tab, Tabs, Grid, CardContent } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard, ColoredText } from "../../components/common/styled";
import CardGrid from "../../components/common/CardGrid";
import ApexCandlestick from "../../components/graph/ApexCandlestick";
import axios from "../../utils/api";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import { format } from "../../utils/formatter";

import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call

const parsedApexData = TimeSeriesData.AAPL.values
  .map(({ datetime, open, close, high, low }) => {
    return { x: new Date(datetime), y: [open, high, low, close] };
  })
  .slice(0, 120);

const StatCard = ({ name, value, stat, today }) => {
  return (
    <StandardCard style={{ minHeight: "130px" }}>
      <CardContent>
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
            <Grid item xs={12}>
              <Typography variant="h4">
                {value ? value : <Skeleton />}
              </Typography>
            </Grid>
            {/* TODO: implement these when backend is ready */}
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
                <Typography variant="caption">Today:</Typography>
              </Grid>
              <Grid item xs={12}>
                <ColoredText
                  variant="subtitle2"
                  color={stat > 0 ? "green" : "red"}
                >
                  {today}
                </ColoredText>
              </Grid>
            </>
          )}
        </Grid>
      </CardContent>
    </StandardCard>
  );
};

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [myValue, setValue] = useState(0);
  const [longData] = useRealTimeStockData(
    "/portfolio",
    [],
    [...Array(12)].map((_) => {
      return { skeleton: true };
    }),
    (d) => d.long
  );
  const [shortData] = useRealTimeStockData(
    "/portfolio",
    [],
    [...Array(12)].map((_) => {
      return { skeleton: true };
    }),
    (d) => d.short
  );
  const [watchData] = useRealTimeStockData("/watchlist", [myValue]);
  // const [balance, setBalance] = useState(0);

  const [stats, setStats] = useState([
    { name: "Portfolio Value", valueKey: "total_portfolio_value" },
    { name: "Net Value", valueKey: "total_value" },
    { name: "Profit", valueKey: "total_portfolio_profit" },
    { name: "Available Balance", valueKey: "balance" },
    // { name: "Net Value", value: 26992.23, stat: 23, today: 2 }, e.g. format
  ]);
  useEffect(() => {
    axios
      .get("/portfolio/stats")
      .then((response) => {
        setStats(
          stats.map(({ valueKey, name }) => {
            return { name: name, value: format(response.data[valueKey]) };
          })
        );
      })
      .catch((err) => console.log(err));
  }, [user]);

  return (
    <Page>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        {stats.map((data, index) => (
          <Grid key={index} item md={3} sm={6} xs={12}>
            <StatCard {...data} />
          </Grid>
        ))}
        <Grid item xs={12}>
          <StandardCard>
            <CardContent>
              <ApexCandlestick data={parsedApexData} />
            </CardContent>
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <Tabs
              value={myValue}
              onChange={(_event, newValue) => {
                console.log("setting value to", newValue);
                setValue(newValue);
              }}
              indicatorColor="primary"
              textColor="primary"
              variant="fullWidth"
            >
              <Tab label="Longs" />
              <Tab label="Shorts" />
              <Tab label="Watchlist" />
            </Tabs>
          </StandardCard>
          <CardGrid
            data={
              myValue === 0 ? longData : myValue === 1 ? shortData : watchData
            }
          />
        </Grid>
      </Grid>
    </Page>
  );
};

export default Dashboard;
