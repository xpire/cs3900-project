import React, { useContext, useState, useEffect } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardContent,
  Chip,
} from "@material-ui/core";

import { format } from "../../utils/formatter";
import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";

const Achievements = () => {
  const { user } = useContext(AuthContext);
  const [data] = useApi("/user/achievements");
  const [userData, userDataLoading] = useApi("/user");
  const [expPercentage, setExpPercentage] = useState(0);
  useEffect(() => {
    if (
      userData &&
      userData.exp_until_next_level &&
      userData.exp_until_next_level !== null
    ) {
      setExpPercentage(
        (userData.exp / (userData.exp_until_next_level + userData.exp)) * 100
      );
    }
  }, [userData]);

  return (
    <Page>
      <StandardCard>
        <CardContent>
          <Typography variant="h2">{user.email}</Typography>
          {!userDataLoading && (
            <Typography>
              Level {userData.level} ({format(expPercentage)}%)
            </Typography>
          )}
          <LinearProgress variant="determinate" value={expPercentage} />
        </CardContent>
      </StandardCard>
      <StandardCard>
        <CardContent>
          <Typography variant="h3">
            Unlocked Achievements: (
            {data.filter(({ is_unlocked }) => is_unlocked).length}/{data.length}
            )
          </Typography>
        </CardContent>
      </StandardCard>
      <Grid container direction="row">
        {data.map(({ id, name, description, is_unlocked, exp }) => {
          return (
            <Grid item xs={12} sm={6} md={4} key={id}>
              <StandardCard>
                <CardContent>
                  <Typography
                    variant="h4"
                    color={is_unlocked ? "primary" : "textPrimary"}
                  >
                    {name}
                  </Typography>
                  <Chip label={`${exp} xp`} size="small" />
                  <Typography>{description}</Typography>
                </CardContent>
              </StandardCard>
            </Grid>
          );
        })}
      </Grid>
      {/* <Typography>{`websocket status: ${connectionStatus}`}</Typography>
      <Typography>{`last json message: ${JSON.stringify(
        lastJsonMessage
      )}`}</Typography> */}

      {/* <Grid container>
        {messageHistory.map((msg, idx) => (
          <Grid item key={idx}>
            <StandardCard>
              <CardContent>
                <span key={idx}>
                  {JSON.stringify(msg)} <br />
                </span>
              </CardContent>
            </StandardCard>
          </Grid>
        ))}
      </Grid> */}
    </Page>
  );
};

export default Achievements;
