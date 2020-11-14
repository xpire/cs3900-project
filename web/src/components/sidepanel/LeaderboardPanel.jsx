import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { format } from "../../utils/formatter";

function LeaderboardPanel() {
  const { rankings, user_ranking } = useSelector(
    (state) => state.user.leaderboard
  );
  return (
    <div>
      <Typography variant="h6">Leaderboard</Typography>
      <Typography variant="subtitle1">
        Your ranking is #{user_ranking}
      </Typography>
      <List>
        <Divider />
        {rankings.map(({ username, net_worth }, index) => {
          return (
            <ListItem divider dense>
              <ListItemText
                primary={`${index + 1}. ${username}`}
                secondary={`$${format(net_worth)}`}
              />
            </ListItem>
          );
        })}
      </List>
    </div>
  );
}

export default LeaderboardPanel;
