import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { useSnackbar, SnackbarContent } from "notistack";
import {
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  makeStyles,
  Grid,
} from "@material-ui/core";
import { useHistory } from "react-router-dom";

import LevelUpIcon from "@material-ui/icons/ArrowUpward";
import UnlockFeatureIcon from "@material-ui/icons/LockOpen";
import UnlockAchievementIcon from "@material-ui/icons/NewReleases";

const useStyles = makeStyles((theme) => ({
  root: {
    [theme.breakpoints.up("sm")]: {
      minWidth: "344px !important",
    },
  },
  card: {
    backgroundColor: "#43a047",
    width: "100%",
  },
}));

/**
 * A SnackBar component custom designed with a subtitle section and an icon
 */
const DetailedSnackbar = React.forwardRef((props, ref) => {
  const classes = useStyles();
  const { closeSnackbar } = useSnackbar();
  let history = useHistory();
  const handleDismiss = () => {
    closeSnackbar(props.id);
  };
  const eventType = props.message.event_type;
  useEffect(() => {
    props.celebrate(true);
    // return () => {
    //   props.celebrate(false);
    // };
  }, []);

  return (
    <SnackbarContent ref={ref} className={classes.root}>
      <Card className={classes.card}>
        <CardContent>
          <Grid container>
            <Grid item xs={2}>
              {eventType === "LEVEL_UP" ? (
                <LevelUpIcon />
              ) : eventType === "ACHIEVMENT_UNLOCKED" ? (
                <UnlockAchievementIcon />
              ) : (
                <UnlockFeatureIcon />
              )}
            </Grid>
            <Grid item xs={10}>
              <Typography variant="subtitle2">
                {eventType === "ACHIEVEMENT_UNLOCKED"
                  ? `${props.message.title} xp`
                  : `${props.message.title}`}
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Typography>{props.message.content}</Typography>
            </Grid>
          </Grid>
        </CardContent>
        <CardActions>
          <Button
            size="small"
            onClick={() => {
              history.push(eventType === "LEVEL_UP" ? "/profile" : "/support");
              handleDismiss();
            }}
          >
            Show me
          </Button>
          <Button size="small" onClick={handleDismiss}>
            OK
          </Button>
        </CardActions>
      </Card>
    </SnackbarContent>
  );
});

export default DetailedSnackbar;
