import React, { useContext } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardActionArea,
  CardContent,
  CardActions,
  Button,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { Link } from "react-router-dom";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import { format } from "../../utils/formatter";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";

const headCells = [
  {
    id: "index",
    formatType: tableTypes.ID,
    disablePadding: false,
    label: "Id",
  },
  {
    id: "timestamp",
    formatType: tableTypes.DATE,
    disablePadding: false,
    label: "Timestamp",
  },
  {
    id: "t_type",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Trade Type",
  },
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
    id: "amount",
    formatType: tableTypes.NUMBER,
    disablePadding: false,
    label: "Quantity",
  },
  {
    id: "price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Price",
  },
  {
    id: "value",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Value",
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

  const [transactionData] = useApi("/transactions");

  const mappedTransactionData = transactionData.map((e, index) => {
    return { ...e, index: index + 1 };
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
                  Level {data.level} (
                  {data.exp_until_next_level === null
                    ? 100
                    : format(
                        (data.exp / (data.exp_until_next_level + data.exp)) *
                          100
                      )}
                  %)
                </Typography>
                <LinearProgress
                  value={
                    data.exp_until_next_level === null
                      ? 100
                      : (data.exp / (data.exp_until_next_level + data.exp)) *
                        100
                  }
                  variant="determinate"
                />
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
              <Typography variant="h3">Graph</Typography>
              <Typography variant="h3">
                <Skeleton />
              </Typography>
            </CardContent>
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <SortableTable
              data={mappedTransactionData}
              header={headCells}
              title="Transaction History"
            />
          </StandardCard>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Profile;
