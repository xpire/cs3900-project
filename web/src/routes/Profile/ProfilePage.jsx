import React, { useContext, useState, useEffect } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardActionArea,
  CardContent,
  CardActions,
  Button,
} from "@material-ui/core";
// import { Skeleton } from "@material-ui/lab";
import { Link } from "react-router-dom";

import InteractiveRefresh from "../../components/common/InteractiveRefresh";
import Cumulative from "../../components/graph/Cumulative";
import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard, BasicCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import { format } from "../../utils/formatter";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";

const columns = [
  {
    field: "timestamp",
    title: (
      <RenderItem title="Timestamp" subtitle="Index" alignItems="flex-start" />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.timestamp}
        titleType={tableTypes.DATE}
        subtitle={rowData.index}
        subtitleType={tableTypes.NUMBER}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "symbol",
    title: <RenderItem title="Symbol" subtitle="Name" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.name}
        subtitleType={tableTypes.TEXT}
      />
    ),
    align: "right",
  },
  {
    field: "trade_type",
    title: <RenderItem title="Trade Type" subtitle="Quantity" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.trade_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.qty}
        subtitleType={tableTypes.NUMBER}
      />
    ),
    align: "right",
  },
  {
    field: "price",
    title: <RenderItem title="Price" subtitle="Value" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.price}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.value}
        subtitleType={tableTypes.CURRENCY}
      />
    ),
    align: "right",
  },
];

const Profile = () => {
  const { user } = useContext(AuthContext);
  const [data] = useApi("/user");
  const [rank] = useApi(
    "/leaderboard",
    [],
    1,
    ({ user_ranking }) => user_ranking
  );

  const [expPercentage, setExpPercentage] = useState(0);
  useEffect(() => {
    if (
      data &&
      data.exp_until_next_level &&
      data.exp_until_next_level !== null
    ) {
      setExpPercentage(
        (data.exp / (data.exp_until_next_level + data.exp)) * 100
      );
    }
  }, [data]);

  const [transactionData, transactionDataLoading] = useApi("/transactions");

  const mappedTransactionData = transactionData.map((e, index) => {
    return { ...e, index: index + 1 };
  });

  const [graphUpdate, setGraphUpdate] = useState(0);
  const [graph, graphLoading] = useApi("/portfolio/history", [], [], (data) => {
    // console.log(data);
    const newData = data.map((e) => [new Date(e.timestamp), e.net_worth]);
    console.log({ data, newData });
    return newData;
  });

  return (
    <Page>
      <Grid container direction="row">
        <Grid item xs={12} sm={12} md={6}>
          <StandardCard>
            <CardActionArea>
              <CardContent>
                <Typography variant="h3">{data.username}</Typography>
                <Typography variant="subtitle2">{user.email}</Typography>
                <Typography variant="h5">Rank: #{rank}</Typography>
                <Typography variant="h5">
                  Net: ${format(data.balance)}
                </Typography>
                <Typography variant="h5">
                  Level {data.level} ({format(expPercentage)}%)
                </Typography>
                <LinearProgress value={expPercentage} variant="determinate" />
              </CardContent>
            </CardActionArea>
            <CardActions>
              <Button
                color="primary"
                variant="outlined"
                component={Link}
                to="/achievements"
              >
                Achievements
              </Button>
              <Button
                color="primary"
                variant="outlined"
                component={Link}
                to="/leaderboard"
              >
                Leaderboard
              </Button>
            </CardActions>
          </StandardCard>
        </Grid>
        <Grid item xs={12} sm={12} md={6}>
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
          <BasicCard>
            <SortableStockTable
              title="Transaction History"
              columns={columns}
              data={mappedTransactionData}
              isLoading={transactionDataLoading}
            />
          </BasicCard>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Profile;
