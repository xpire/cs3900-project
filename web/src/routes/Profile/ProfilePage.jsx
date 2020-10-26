import React, { useContext, useState, useEffect } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardActionArea,
  Card,
  CardContent,
  CardActions,
  Button,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { Link } from "react-router-dom";

import { AuthContext } from "../../utils/authentication";
import axios from "../../utils/api";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import { format } from "../../utils/formatter";

const Profile = () => {
  const { user } = useContext(AuthContext);
  const [data] = useApi("/user");
  const [rank] = useApi(
    "/leaderboard",
    [],
    1,
    ({ user_ranking }) => user_ranking
  );
  // const [data, setData] = useState({});
  // useEffect(() => {
  //   axios.get("/user").then((response) => {
  //     console.log(response.data);
  //     setData(response.data);
  //   });
  // }, []);
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
            <CardContent>
              <Typography variant="h2">Transaction History</Typography>
              <Skeleton />
            </CardContent>
          </StandardCard>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Profile;
