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
import { Link } from "react-router-dom";
import {
  formatToCurrency,
  format,
  formatWithPlus,
} from "../../utils/formatter";
import { HalfGridItem } from "./Common";
import ScrollPanel from "./ScrollablePanel";
import ColoredText, { useColoredText } from "../common/ColoredText";

function NumericColoredText({
  value,
  text,
  fontSize,
  color,
  showTxtColor = true,
}) {
  return (
    <div style={{ textAlign: "right" }}>
      <ColoredText
        color={showTxtColor ? (value > 0 ? "green" : "red") : null}
        style={{ fontSize, display: "inline" }}
        delta={color}
        align="right"
      >
        {text}
      </ColoredText>
    </div>
  );
}

function WatchlistItem({ symbol, price, change, changePercentage }) {
  const [color] = useColoredText(price);

  const priceTxt = `${formatToCurrency(price)}`;
  const changeTxt = `${formatWithPlus(changePercentage)}% ${formatToCurrency(
    change
  )} `;

  return (
    <ListItem
      divider
      dense
      key={symbol}
      button
      component={Link}
      to={`/stock/${symbol}`}
    >
      <Grid container>
        <Grid item xs={5}>
          <Typography style={{ fontSize: 14 }}>{symbol}</Typography>
        </Grid>
        <Grid item xs={7}>
          <NumericColoredText
            value={price}
            text={priceTxt}
            fontSize={14}
            color={color}
            showTxtColor={false}
          />
          <NumericColoredText
            value={change}
            text={changeTxt}
            fontSize={11}
            color={color}
          />
        </Grid>
      </Grid>
    </ListItem>
  );
}

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
        const changePercentage = change / open;

        return (
          <WatchlistItem {...{ symbol, price, change, changePercentage }} />
        );
      })}
    </List>
  );
  return <ScrollPanel title={title} content={content} />;
}

export default WatchlistPanel;
