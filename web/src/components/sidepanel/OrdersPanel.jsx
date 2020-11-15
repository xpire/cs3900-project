import React from "react";
import { List, ListItem, Typography, Tooltip } from "@material-ui/core";
import { Link } from "react-router-dom";

import { useColoredText } from "../common/ColoredText";

import {
  format,
  formatToCurrency,
  formatWithPlus,
} from "../../utils/formatter";
import { useSelector } from "react-redux";
import { PanelTab } from "./PanelTab";
import { getOrders, getTransactions } from "../../reducers/index";
import {
  NumericColoredText,
  VALUE_SIZE,
  SUBVALUE_SIZE,
  PanelListHeader,
  PanelListItem,
  ComputeChanges,
} from "./Common";

function OrderListItem({
  symbol,
  qty,
  limit_price,
  trade_type,
  order_type,
  price,
  change,
  changePercentage,
}) {
  const [color] = useColoredText(price);
  const priceTxt = `${formatToCurrency(price)}`;
  const changeTxt = `${formatWithPlus(changePercentage)}% / ${formatToCurrency(
    change
  )} `;

  const order_price =
    order_type === "LIMIT" ? formatToCurrency(limit_price) : "market";
  const order = `${trade_type.toLowerCase()} ${qty} @ ${order_price}`;

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
      <Typography color="textSecondary" style={{ fontSize: SUBVALUE_SIZE }}>
        {order}
      </Typography>
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
    >
      <PanelListItem {...frags} />
    </ListItem>
  );
}

function OrdersTable({ orders, stocks, tabValue }) {
  return (
    <List style={{ paddingTop: "0px" }}>
      {orders.map(
        ({ id, symbol, qty, limit_price, trade_type, order_type }) => {
          const { curr_day_close: price, curr_day_open: open } = stocks[symbol];
          const [change, changePercentage] = ComputeChanges(price, open);

          return (
            <OrderListItem
              key={`OrderListItem-${tabValue}-${id}`}
              {...{
                symbol,
                qty,
                limit_price,
                trade_type,
                order_type,
                price,
                change,
                changePercentage,
              }}
            />
          );
        }
      )}
    </List>
  );
}

function TransactionsListItem({
  symbol,
  qty,
  price,
  timestamp,
  order_type,
  trade_type,
  is_cancelled,
}) {
  const order_price =
    order_type === "LIMIT" ? formatToCurrency(price) : "market";
  const order = `${trade_type.toLowerCase()} ${qty} @ ${order_price}`;
  const exec_price = !is_cancelled ? formatToCurrency(price) : "cancelled";
  const date = new Date(timestamp);

  const frags = {
    frag1: <Typography style={{ fontSize: VALUE_SIZE }}>{symbol}</Typography>,
    frag2: (
      <Typography style={{ fontSize: VALUE_SIZE }}>{exec_price}</Typography>
    ),
    subfrag1: (
      <Typography color="textSecondary" style={{ fontSize: SUBVALUE_SIZE }}>
        {order}
      </Typography>
    ),
    subfrag2: (
      <Tooltip title={`${date.toLocaleString()}`}>
        <Typography color="textSecondary" style={{ fontSize: SUBVALUE_SIZE }}>
          {date.toLocaleDateString()}
        </Typography>
      </Tooltip>
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

function TransactionsTable({ data, tabValue }) {
  return (
    <List style={{ paddingTop: "0px" }}>
      {data.map(({ id, ...rest }) => {
        return (
          <TransactionsListItem
            key={`TransactionsListItem-${tabValue}-${id}`}
            {...rest}
          />
        );
      })}
    </List>
  );
}

function OrdersPanel() {
  const orders = useSelector(getOrders);
  const transactions = useSelector(getTransactions);
  const stocks = useSelector((state) => state.stocks.dict);

  const ordersLabels = {
    label1: "Symbol",
    sublabel1: "Order", // E.g. BUY 10 @ market
    label2: "Market Price",
    sublabel2: "CHG%/CHG",
  };

  const transLabels = {
    label1: "Symbol",
    sublabel1: "Order",
    label2: "Execution Price", // BUY SELL SHORT COVER
    sublabel2: "Timestamp", // Price or Cancelled
  };

  const tab1 = {
    label: "Orders",
    subtitle: <PanelListHeader {...ordersLabels} />,
    content: <OrdersTable orders={orders} stocks={stocks} />,
  };
  const tab2 = {
    label: "Transactions",
    subtitle: <PanelListHeader {...transLabels} />,
    content: <TransactionsTable data={transactions} />,
  };

  return <PanelTab tab1={tab1} tab2={tab2} />;
}

export default OrdersPanel;
