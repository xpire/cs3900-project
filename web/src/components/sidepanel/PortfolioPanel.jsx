import React, { useState, useEffect } from "react";
import { List, ListItem, Typography, Grid } from "@material-ui/core";
import { formatToCurrency, formatWithPlus } from "../../utils/formatter";
import { useSelector } from "react-redux";
import { PanelTab } from "./PanelTab";
import { Link } from "react-router-dom";
import { useColoredText } from "../common/ColoredText";
import {
  NumericColoredText,
  VALUE_SIZE,
  SUBVALUE_SIZE,
  PanelListHeader,
  PanelListItem,
  ComputeChanges,
} from "./Common";

function PortfolioListItem({
  symbol,
  price,
  qty,
  change,
  changePercentage,
  tabValue,
}) {
  const [color] = useColoredText(price);
  const [qtyColor] = useColoredText(qty);

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
    subfrag1: (
      <NumericColoredText
        value={qty}
        text={qty}
        fontSize={SUBVALUE_SIZE}
        color={qtyColor}
        align="left"
        showTxtColor={false}
      />
    ),
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
      key={`ListItem-${tabValue}-${symbol}`}
    >
      <PanelListItem {...frags} />
    </ListItem>
  );
}

function PortfolioTable({ data, tabValue }) {
  return (
    <List style={{ paddingTop: "0px" }}>
      {data.map(({ symbol, price, previous_price: open, owned: qty }) => {
        const [change, changePercentage] = ComputeChanges(price, open);
        return (
          <PortfolioListItem
            key={`PortfolioListItem-${tabValue}-${symbol}`}
            {...{ symbol, price, qty, change, changePercentage, tabValue }}
          />
        );
      })}
    </List>
  );
}

function PortfolioPanel() {
  const { long, short } = useSelector((state) => state.user.portfolio);

  const labels = {
    label1: "Symbol",
    sublabel1: "Shares",
    label2: "Market Price",
    sublabel2: "CHG%/CHG",
  };

  const header = <PanelListHeader {...labels} />;
  const tab1 = {
    label: "Longs",
    subtitle: header,
    content: <PortfolioTable data={long} tabValue={0} />,
  };
  const tab2 = {
    label: "Shorts",
    subtitle: header,
    content: <PortfolioTable data={short} tabValue={1} />,
  };

  return <PanelTab tab1={tab1} tab2={tab2} />;
}

export default PortfolioPanel;
