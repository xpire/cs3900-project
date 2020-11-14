import React from "react";
import { Typography } from "@material-ui/core";

import { format } from "../../utils/formatter";
import { useSelector } from "react-redux";
import { PanelTab } from "./PanelTab";

function OrdersTable({ orders, stocks }) {
  return (
    <div>
      {[...orders]
        .reverse()
        .map(({ symbol, qty, order_type, trade_type, limit_price }) => {
          const msg =
            order_type === "LIMIT"
              ? `${trade_type} ${qty} of ${symbol} @ $${format(limit_price)}`
              : `${trade_type} ${qty} of ${symbol} @ market open`;
          const price = "$" + format(stocks[symbol].curr_day_close);
          return <Typography>{msg + " current price: " + price}</Typography>;
        })}
    </div>
  );
}

function TransactionsTable({ data }) {
  return (
    <div>
      {[...data]
        .reverse()
        .map(({ symbol, qty, price, trade_type, is_cancelled }) => {
          const prefix = is_cancelled ? "Cancelled" : "Executed";
          const detail = `${trade_type} ${qty} of ${symbol} @ $${format(
            price
          )}`;
          const msg = prefix + ": " + detail;
          return <Typography>{msg}</Typography>;
        })}
    </div>
  );
}

function OrdersPanel() {
  const orders = useSelector((state) => state.user.orders);
  const transactions = useSelector((state) => state.user.transactions);
  const stocks = useSelector((state) => state.stocks.dict);

  const tab1 = {
    label: "Orders",
    content: <OrdersTable orders={orders} stocks={stocks} />,
  };
  const tab2 = {
    label: "Transactions",
    content: <TransactionsTable data={transactions} />,
  };

  if (orders) {
    return <PanelTab tab1={tab1} tab2={tab2} />;
  }
  return <div></div>;
}

export default OrdersPanel;
