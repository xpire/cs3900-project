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

const VALUE_SIZE = 14;
const SUBVALUE_SIZE = 11;
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
  const changeTxt = `${formatWithPlus(changePercentage)}% / ${formatToCurrency(
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
          <Typography style={{ fontSize: VALUE_SIZE }}>{symbol}</Typography>
        </Grid>
        <Grid item xs={7}>
          <NumericColoredText
            value={price}
            text={priceTxt}
            fontSize={VALUE_SIZE}
            color={color}
            showTxtColor={false}
          />
          <NumericColoredText
            value={change}
            text={changeTxt}
            fontSize={SUBVALUE_SIZE}
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

  const title = (
    <>
      <Typography variant="h6">Watchlist</Typography>
      <div style={{ padding: "0px 16px 4px 16px" }}>
        <Grid container>
          <Grid item xs={5}>
            <Typography style={{ fontSize: VALUE_SIZE }}>Symbol</Typography>
          </Grid>
          <Grid item xs={7}>
            <div style={{ textAlign: "right" }}>
              <Typography style={{ fontSize: VALUE_SIZE }}>Price</Typography>
              <Typography
                color="textSecondary"
                style={{ fontSize: SUBVALUE_SIZE }}
              >
                CHG%/CHG
              </Typography>
            </div>
          </Grid>
        </Grid>
      </div>
      <Divider />
      <Divider />
    </>
  );
  const content = (
    <List style={{ paddingTop: "0px" }}>
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
