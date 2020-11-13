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

function WatchlistPanel() {
  const watchlist = useSelector((state) => state.user.watchlist);
  return (
    <div>
      <Typography>Watchlist</Typography>
      <List>
        <Divider />
        {watchlist.map(({ symbol, curr_day_close: price }) => {
          const msg = `${symbol} is @$${format(price)}`;
          return (
            <ListItem divider dense>
              <ListItemText primary={msg} />
            </ListItem>
          );
        })}
      </List>
    </div>
  );
}

export default WatchlistPanel;
