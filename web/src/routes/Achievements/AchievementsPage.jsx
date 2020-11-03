import React, { useContext } from "react";
import {
  Typography,
  Grid,
  LinearProgress,
  CardContent,
  Chip,
} from "@material-ui/core";

// import useSockets from "../../hooks/useSockets";
import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";

const Achievements = () => {
  const { user } = useContext(AuthContext);

  // const [lastJsonMessage, messageHistory, connectionStatus] = useSockets();
  // const [achievements, setAchievements] = useState([]);

  // useEffect(() => {
  //   axios.get("/user/achievements").then((response) => {
  //     setAchievements(response.data);
  //     console.log(response.data);
  //   });
  // }, []);

  const [data] = useApi("/user/achievements");

  return (
    <Page>
      <StandardCard>
        <CardContent>
          <Typography variant="h2">{user.email}</Typography>
          <Typography>{`Level ${5}`}</Typography>
          <LinearProgress variant="determinate" value={40} />
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
                    color={is_unlocked ? "primary" : "primaryText"}
                  >
                    {name}
                  </Typography>
                  <Chip label={`${exp} xp`} />
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
