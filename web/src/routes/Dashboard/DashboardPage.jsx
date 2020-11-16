import React, { useContext, useState, useEffect } from "react";
import {
  Typography,
  Tab,
  Tabs,
  Grid,
  CardContent,
  IconButton,
} from "@material-ui/core";
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
import { format, formatToCurrency } from "../../utils/formatter";
import { useSelector } from "react-redux";
import {
  getPortfolioRealTimeData,
  getWatchlistRealTimeData,
} from "../../reducers";
import { makeSkeleton } from "../../utils/skeleton";

const CardsSpaceDiv = styled.div`
  // min-height: 75vh;
  min-height: 100vh;
`;

const StatCard = ({
  label,
  value,
  percentageValue = undefined,

  subLabel = undefined,
  subValue = undefined,
  subPercentageValue = undefined,
  subNegative = undefined,

  subsubLabel = undefined,
  subsubValue = undefined,
  subsubPercentageValue = undefined,
  subsubNegative = undefined,
}) => {
  const [valueDelta] = useColoredText(value);
  const [subValueDelta] = useColoredText(subValue);
  const [subsubValueDelta] = useColoredText(subsubValue);

  console.log({
    label,
    value,
    percentageValue,
    subLabel,
    subValue,
    subPercentageValue,
    subsubLabel,
    subsubValue,
    subsubPercentageValue,
  });

  return (
    <StandardCard style={{ minHeight: "130px", height: "90%" }}>
      <CardContent>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
        >
          <Grid item xs={12}>
            <Typography variant="button">{label}</Typography>
          </Grid>
          <Grid item xs={12} container justify="flex-start" spacing={0}>
            {value !== undefined && (
              <Grid item>
                <ColoredText delta={valueDelta} variant="h4">
                  {formatToCurrency(value)}
                </ColoredText>
              </Grid>
            )}
            {percentageValue !== undefined && (
              <Grid item>
                <ColoredText delta={valueDelta} variant="body2">
                  {format(100 * percentageValue)}
                </ColoredText>
              </Grid>
            )}
          </Grid>
          <Grid
            item
            xs={
              subsubValue !== undefined ||
              subsubPercentageValue !== undefined ||
              subsubLabel !== undefined
                ? 6
                : 12
            }
            container
            justify="flex-start"
            direction="column"
            spacing={0}
          >
            {subLabel !== undefined && (
              <Grid item xs={12}>
                <Typography delta={subValueDelta} variant="button">
                  {subLabel}
                </Typography>
              </Grid>
            )}
            {subValue !== undefined && (
              <Grid item>
                <ColoredText
                  delta={
                    subNegative !== undefined && subNegative
                      ? -subValueDelta
                      : subValueDelta
                  }
                  variant="body2"
                >
                  ${format(subValue)}
                </ColoredText>
              </Grid>
            )}
            {subPercentageValue !== undefined && (
              <Grid item>
                <ColoredText
                  delta={
                    subNegative !== undefined && subNegative
                      ? -subValueDelta
                      : subValueDelta
                  }
                  color={
                    (subPercentageValue > 0 && !subNegative) ||
                    (subPercentageValue <= 0 && !!subNegative)
                      ? "green"
                      : "red"
                  }
                  variant="body2"
                >
                  ({format(100 * subPercentageValue)}%)
                </ColoredText>
              </Grid>
            )}
          </Grid>
          <Grid
            item
            container
            justify="flex-start"
            direction="column"
            xs={6}
            spacing={0}
          >
            {subsubLabel !== undefined && (
              <Grid item xs={12}>
                <Typography variant="button">{subsubLabel}</Typography>
              </Grid>
            )}
            {subsubValue !== undefined && (
              <Grid item>
                <ColoredText
                  delta={
                    subsubNegative !== undefined && subsubNegative
                      ? -subsubValueDelta
                      : subsubValueDelta
                  }
                  variant="body2"
                >
                  ${format(subsubValue)}
                </ColoredText>
              </Grid>
            )}
            {subsubPercentageValue !== undefined && (
              <Grid item>
                <ColoredText
                  delta={
                    subsubNegative !== undefined && subsubNegative
                      ? -subsubValueDelta
                      : subsubValueDelta
                  }
                  variant="body2"
                  color={
                    (subsubPercentageValue > 0 && !subsubNegative) ||
                    (subsubPercentageValue <= 0 && !!subsubNegative)
                      ? "green"
                      : "red"
                  }
                >
                  ({format(subsubPercentageValue)}%)
                </ColoredText>
              </Grid>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </StandardCard>
  );
};

const statCells = [
  { label: "Net Worth", key: "total_value" },
  {
    label: "Balance",
    key: "balance",
    subLabel: "Short Balance",
    subKey: "short_balance",
  },
  {
    label: "Portfolio Value",
    key: "total_portfolio_value",
    percentageKey: "total_return",
    subLabel: "Longs",
    subKey: "total_long_value",
    subPercentageKey: "total_long_return",
    subsubLabel: "Shorts",
    subsubKey: "total_short_value",
    subsubPercentageKey: "total_short_return",
  },
  {
    label: "Profit",
    key: "total_portfolio_profit",
    subLabel: "Daily",
    subKey: "daily_portfolio_profit",
    subPercentageKey: "daily_portfolio_return",
  },
];

const Dashboard = () => {
  // Main statistics
  const stats = useSelector((state) => state.user.stats);
  const [statCards, setStatCards] = useState(null);
  useEffect(
    () =>
      setStatCards(
        <Grid container>
          {statCells.map((cell, index) => (
            <Grid key={index} item lg={3} md={6} sm={6} xs={12}>
              <StatCard
                label={cell.label}
                value={stats[cell.key]}
                percentageValue={stats[cell.percentageKey]}
                subLabel={cell.subLabel}
                subValue={stats[cell.subKey]}
                subPercentageValue={stats[cell.subPercentageKey]}
                subNegative={cell.subNegative ?? false}
                subsubLabel={cell.subsubLabel}
                subsubValue={stats[cell.subsubKey]}
                subsubPercentageValue={stats[cell.subsubPercentageKey]}
                subsubNegative={cell.subsubNegative ?? false}
              />
            </Grid>
          ))}
        </Grid>
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
  const [graph, graphLoading] = useApi(
    "/portfolio/history",
    [graphUpdate],
    [],
    (data) => data.map((e) => [new Date(e.timestamp), e.net_worth])
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
                  <IconButton onClick={() => setGraphUpdate(graphUpdate + 1)}>
                    <InteractiveRefresh />
                  </IconButton>
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
