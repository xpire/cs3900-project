import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
  Grid,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { formatToCurrency, format } from "../../utils/formatter";
import { HalfGridItem } from "./Common";
import ScrollPanel from "./ScrollablePanel";

function WatchlistPanel() {
  const [watchlist, stocks] = useSelector((state) => [
    state.user.watchlist,
    state.stocks.dict,
  ]);

  const title = <Typography variant="h6">Watchlist</Typography>;
  const content = (
    <List>
      <Divider />
      {watchlist.map(({ symbol }) => {
        const price = stocks[symbol].curr_day_close;
        const open = stocks[symbol].curr_day_open;
        const change = price - open;
        const changePercentange = change / open;

        return (
          <ListItem divider dense key={symbol}>
            <Grid container>
              <Grid item xs={5}>
                <Typography style={{ fontSize: 14 }}>{symbol}</Typography>
              </Grid>
              <Grid item xs={7}>
                <Typography align="right" style={{ fontSize: 14 }}>
                  {formatToCurrency(price)}
                </Typography>
                <Typography align="right" style={{ fontSize: 11 }}>
                  {format(changePercentange)}% {formatToCurrency(change)}
                </Typography>
              </Grid>
            </Grid>
          </ListItem>
        );
      })}
    </List>
  );
  return <ScrollPanel title={title} content={content} />;
}

export default WatchlistPanel;
