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
  const [watchlist, stocks] = useSelector((state) => [
    state.user.watchlist,
    state.stocks.dict,
  ]);

  // const state = useSelect((state) => state.stocks);
  // console.log(state.stocks);
  // console.log(stocks);
  return (
    <div>
      <Typography>Watchlist</Typography>
      <List>
        <Divider />
        {watchlist.map(({ symbol }) => {
          const price = stocks[symbol].curr_day_close;
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
