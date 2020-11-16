import React, { useContext, useState, useEffect } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardActionArea,
  CardContent,
  CardActions,
  Button,
  Chip,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { Link } from "react-router-dom";

import InteractiveRefresh from "../../components/common/InteractiveRefresh";
import Cumulative from "../../components/graph/Cumulative";
import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard, BasicCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import { format } from "../../utils/formatter";
import SortableStockTable, {
  tableTypes,
  RenderItem,
} from "../../components/common/SortableStockTable";
import { useSelector } from "react-redux";
import { makeSkeleton } from "../../utils/skeleton";

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

  const [graphUpdate, setGraphUpdate] = useState(0);
  const [graph, graphLoading] = useApi("/portfolio/history", [], [], (data) =>
    data.map((e) => [new Date(e.timestamp), e.net_worth])
  );

  const [achievementsData] = useApi("/user/achievements", [], makeSkeleton(21));

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
            </CardContent>
            {!graphLoading && <Cumulative data={graph} />}
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <BasicCard>
            <CardContent>
              <Typography variant="h3">
                Unlocked Achievements: (
                {
                  achievementsData.filter(({ is_unlocked }) => is_unlocked)
                    .length
                }
                /{achievementsData.length})
              </Typography>
            </CardContent>
          </BasicCard>
        </Grid>
        <Grid container direction="row">
          {achievementsData.map(
            ({ id, name, description, is_unlocked, exp, skeleton }) => {
              return (
                <Grid item xs={12} sm={6} md={4} key={id}>
                  <StandardCard>
                    <CardActionArea disabled={!is_unlocked || skeleton}>
                      <CardContent>
                        <Typography
                          variant="h4"
                          color={is_unlocked ? "primary" : "textPrimary"}
                        >
                          {skeleton ? <Skeleton /> : name}
                        </Typography>
                        {!skeleton && <Chip label={`${exp} xp`} size="small" />}
                        <Typography>
                          {skeleton ? <Skeleton /> : description}
                        </Typography>
                      </CardContent>
                    </CardActionArea>
                  </StandardCard>
                </Grid>
              );
            }
          )}
        </Grid>
      </Grid>
    </Page>
  );
};

export default Profile;
