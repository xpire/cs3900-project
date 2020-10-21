import React, { useContext } from "react";
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
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";

const Profile = () => {
  const { user } = useContext(AuthContext);
  return (
    <Page>
      <Grid container direction="row">
        <Grid item xs={12} sm={12} md={6}>
          <StandardCard>
            <CardActionArea>
              <CardContent>
                <Typography variant="h3">{user.email}</Typography>
                <Typography variant="h5">Rank: #{5}</Typography>
                <Typography variant="h5">Net: ${1234567890.12}</Typography>
                <Typography variant="h5">Level {6}</Typography>
                <LinearProgress value={45} variant="determinate" />
              </CardContent>
            </CardActionArea>
            <CardActions>
              <Button>More info</Button>
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
