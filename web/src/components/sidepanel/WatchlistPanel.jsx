import { List, ListItem, Typography } from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { formatToCurrency, formatWithPlus } from "../../utils/formatter";
import ScrollPanel from "./ScrollablePanel";
import { useColoredText } from "../common/ColoredText";
import {
  NumericColoredText,
  VALUE_SIZE,
  SUBVALUE_SIZE,
  PanelListHeader,
  PanelListItem,
  ComputeChanges,
} from "./Common";

function WatchlistItem({ symbol, price, change, changePercentage }) {
  const [color] = useColoredText(price);

  const priceTxt = `${formatToCurrency(price)}`;
  const changeTxt = `${formatWithPlus(changePercentage)}% / ${formatToCurrency(
    change
  )} `;

  const frags = {
    frag1: <Typography style={{ fontSize: VALUE_SIZE }}>{symbol}</Typography>,
    frag2: (
      <NumericColoredText
        value={price}
        text={priceTxt}
        fontSize={VALUE_SIZE}
        color={color}
        showTxtColor={false}
      />
    ),
    subfrag1: null,
    subfrag2: (
      <NumericColoredText
        value={change}
        text={changeTxt}
        fontSize={SUBVALUE_SIZE}
        color={color}
      />
    ),
  };

  return (
    <ListItem
      divider
      dense
      key={symbol}
      button
      component={Link}
      to={`/stock/${symbol}`}
    >
      <PanelListItem {...frags} />
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
      <PanelListHeader
        label1="Symbol"
        label2="Market Price"
        sublabel2="CHG%/CHG"
      />
    </>
  );
  const content = (
    <List style={{ paddingTop: "0px" }}>
      {watchlist.map(({ symbol }) => {
        const price = stocks[symbol].curr_day_close;
        const open = stocks[symbol].curr_day_open;
        const [change, changePercentage] = ComputeChanges(price, open);
        return (
          <WatchlistItem
            key={symbol}
            {...{ symbol, price, change, changePercentage }}
          />
        );
      })}
    </List>
  );
  return <ScrollPanel title={title} content={content} />;
}

export default WatchlistPanel;
