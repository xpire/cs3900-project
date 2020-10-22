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

import { AuthContext } from "../../utils/authentication";
import axios from "../../utils/api";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";

const Profile = () => {
  const { user } = useContext(AuthContext);
  const [data, setData] = useState({});
  useEffect(() => {
    axios.get("/user").then((response) => {
      console.log(response.data);
      setData(response.data);
    });
  }, []);
  return (
    <Page>
      <Grid container direction="row">
        <Grid item xs={12} sm={12} md={6}>
          <StandardCard>
            <CardActionArea>
              <CardContent>
                <Typography variant="h3">{user.email}</Typography>
                {/* <Typography variant="h5">Rank: #{5}</Typography> */}
                <Typography variant="h5">Net: ${data.balance}</Typography>
                <Typography variant="h5">
                  Level {data.level} (
                  {(data.exp / (data.exp_until_next_level + data.exp)) * 100}%)
                </Typography>
                <LinearProgress
                  value={
                    (data.exp / (data.exp_until_next_level + data.exp)) * 100
                  }
                  variant="determinate"
                />
              </CardContent>
            </CardActionArea>
            <CardActions>
              <Button color="primary" variant="outlined">
                Achievements
              </Button>
              <Button color="primary" variant="outlined">
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
              hello
            </CardContent>
          </StandardCard>
        </Grid>
      </Grid>
    </Page>
  );
};

export default Profile;
