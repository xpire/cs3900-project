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
import { useSelector } from "react-redux";
import {
  getPortfolioRealTimeData,
  getWatchlistRealTimeData,
} from "../../reducers";

const CardsSpaceDiv = styled.div`
  // min-height: 75vh;
  min-height: 100vh;
`;

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

const makeSkeleton = (n) =>
  [...Array(n)].map((_) => {
    return { skeleton: true };
  });

const statCells = [
  { label: "Net Worth", id: "total_value" },
  { label: "Balance", id: "balance" },
  { label: "Portfolio Value", id: "total_portfolio_value" },
  { label: "Profit", id: "total_portfolio_profit" },
];

const Dashboard = () => {
  // Main statistics
  const stats = useSelector((state) => state.user.stats);
  const [statCards, setStatCards] = useState(null);
  useEffect(
    () =>
      setStatCards(
        statCells.map((cell, index) => (
          <Grid key={index} item lg={3} md={6} sm={6} xs={12}>
            <StatCard name={cell.label} value={format(stats[cell.id])} />
          </Grid>
        ))
      ),
    [stats]
  );

  // Card data
  const [tabValue, setValue] = useState(0);
  const isUserLoading = useSelector((state) => state.user.is_loading);
  const isStocksLoading = useSelector((state) => state.stocks.is_loading);
  const isLoading = (isUserLoading ?? true) || (isStocksLoading ?? true);
  const { long, short } = useSelector(getPortfolioRealTimeData);
  const watchlist = useSelector(getWatchlistRealTimeData);

  const longData = isLoading ? makeSkeleton(12) : long;
  const shortData = isLoading ? makeSkeleton(12) : short;
  const watchData = isLoading ? makeSkeleton(12) : watchlist;

  // Networth graph
  const [graphUpdate, setGraphUpdate] = useState(0);
  const [graph, graphLoading] = useApi("/portfolio/history", [], [], (data) =>
    data.map((e) => [new Date(e.timestamp), e.net_worth])
  );

  return (
    <Page>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        {statCards}
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
              {!graphLoading ? (
                <Cumulative data={graph} />
              ) : (
                <Skeleton variant="rect" height={350} />
              )}
            </CardContent>
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <CardContent>
              <Grid container alignItems="center" justify="space-between">
                <Grid item>
                  <Typography variant="button">
                    Portfolio and Watchlist
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
            <Tabs
              value={tabValue}
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
                tabValue === 0
                  ? longData
                  : tabValue === 1
                  ? shortData
                  : watchData
              }
              watchButton={false}
            />
          </CardsSpaceDiv>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Dashboard;
