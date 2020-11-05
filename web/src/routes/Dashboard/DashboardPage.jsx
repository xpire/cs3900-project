import React, { useContext, useState, useEffect } from "react";
import { Typography, Tab, Tabs, Grid, CardContent } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import styled from "styled-components";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import ColoredText, {
  useColoredText,
} from "../../components/common/ColoredText";
import InteractiveRefresh from "../../components/common/InteractiveRefresh";
import CardGrid from "../../components/common/CardGrid";
import Cumulative from "../../components/graph/Cumulative";
import axios from "../../utils/api";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import useApi from "../../hooks/useApi";
import { format } from "../../utils/formatter";

// import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call

const CardsSpaceDiv = styled.div`
  // min-height: 75vh;
  min-height: 100vh;
`;

// const parsedApexData = TimeSeriesData.AAPL.values
//   .map(({ datetime, open, close, high, low }) => {
//     // return { x: new Date(datetime), y: [open, high, low, close] };
//     return [new Date(datetime), open];
//   })
//   .slice(0, 120);

const StatCard = ({ name, value, stat, today }) => {
  const [delta] = useColoredText(stat);
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
            {/* TODO: implement these extra statistics when backend is ready */}
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
                  delta={delta}
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
  const [forceUpdate, setForceUpdate] = useState({
    long: 0,
    short: 0,
    watch: 0,
  });
  const [longData] = useRealTimeStockData(
    "/portfolio",
    [forceUpdate.long],
    [...Array(12)].map((_) => {
      return { skeleton: true };
    }),
    (d) => d.long
  );
  const [shortData] = useRealTimeStockData(
    "/portfolio",
    [forceUpdate.short],
    [...Array(12)].map((_) => {
      return { skeleton: true };
    }),
    (d) => d.short
  );

  const [watchData] = useRealTimeStockData("/watchlist", [forceUpdate.watch]);

  const [graphUpdate, setGraphUpdate] = useState(0);
  const [graph, graphLoading] = useApi("/portfolio/history", [], [], (data) => {
    // console.log(data);
    const newData = data.map((e) => [new Date(e.timestamp), e.net_worth]);
    console.log({ data, newData });
    return newData;
  });

  const [stats, setStats] = useState([
    { name: "Portfolio Value", valueKey: "total_portfolio_value" },
    { name: "Net Value", valueKey: "total_value" },
    { name: "Profit", valueKey: "total_portfolio_profit" },
    { name: "Available Balance", valueKey: "balance" },
  ]);
  useEffect(() => {
    axios
      .get("/portfolio/stats")
      .then((response) => {
        setStats((s) =>
          s.map(({ valueKey, name }) => {
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
              <Grid container justify="space-between" alignItems="center">
                <Grid item>
                  <Typography variant="button">Cumulative Graph</Typography>
                </Grid>

                <Grid item>
                  <InteractiveRefresh
                    onClick={() => setGraphUpdate(graphUpdate + 1)}
                  />
                </Grid>
              </Grid>
              {!graphLoading && <Cumulative data={graph} />}
            </CardContent>
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <CardContent>
              <Grid container alignItems="center" justify="space-between">
                <Grid item>
                  <Typography variant="button">Positions</Typography>
                </Grid>
                <Grid item>
                  <InteractiveRefresh
                    onClick={() => {
                      switch (myValue) {
                        case 0:
                          setForceUpdate({
                            ...forceUpdate,
                            long: forceUpdate.long + 1,
                          });
                          break;
                        case 1:
                          setForceUpdate({
                            ...forceUpdate,
                            long: forceUpdate.short + 1,
                          });
                          break;
                        case 2:
                          setForceUpdate({
                            ...forceUpdate,
                            long: forceUpdate.watch + 1,
                          });
                          break;
                        default:
                      }
                      // myValue === 0
                      // ? forceUpdate.long + 1
                      // : myValue === 1
                      // ? forceUpdate.short + 1
                      // : forceUpdate.watch
                    }}
                  />
                </Grid>
              </Grid>
            </CardContent>
            <Tabs
              value={myValue}
              onChange={(_event, newValue) => {
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
          <CardsSpaceDiv>
            <CardGrid
              data={
                myValue === 0 ? longData : myValue === 1 ? shortData : watchData
              }
            />
          </CardsSpaceDiv>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Dashboard;
