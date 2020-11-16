import React, { useState } from "react";
import { Card, Tabs, Tab } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableStockTable, {
  tableTypes,
  RenderItem,
} from "../../components/common/SortableStockTable";
import useApi from "../../hooks/useApi";
import useHandleSnack from "../../hooks/useHandleSnack";
import { useDispatch, useSelector } from "react-redux";
import {
  getOrders,
  getTransactions,
  removeFromOrdersWithSnack,
} from "../../reducers";

const columns = [
  {
    field: "timestamp",
    title: (
      <RenderItem title="Timestamp" subtitle="Index" alignItems="flex-start" />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.timestamp}
        titleType={tableTypes.DATE}
        subtitle={rowData.id}
        subtitleType={tableTypes.NUMBER}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "symbol",
    title: <RenderItem title="Symbol" subtitle="Name" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.name}
        subtitleType={tableTypes.TEXT}
      />
    ),
    align: "right",
  },
  {
    field: "trade_type",
    title: <RenderItem title="Trade Type" subtitle="Quantity" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.trade_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.qty}
        subtitleType={tableTypes.SHARES}
      />
    ),
    align: "right",
  },
];

const orderColumns = [
  ...columns,
  {
    field: "order_type",
    title: <RenderItem title="Order Type" subtitle="(Limit Price)" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.order_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.order_type === "LIMIT" ? rowData.limit_price : ""}
        subtitleType={
          rowData.order_type === "LIMIT" ? tableTypes.CURRENCY : tableTypes.TEXT
        }
      />
    ),
    align: "right",
  },
];

const transactionsColumns = [
  ...columns,
  {
    field: "price",
    title: <RenderItem title="Execution Price" subtitle="Value" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.is_cancelled === true ? "Cancelled" : rowData.price}
        titleType={
          rowData.is_cancelled === true ? tableTypes.TEXT : tableTypes.CURRENCY
        }
        subtitle={rowData.is_cancelled === true ? undefined : rowData.value}
        subtitleType={
          rowData.is_cancelled === true ? undefined : tableTypes.CURRENCY
        }
      />
    ),
    align: "right",
  },
];

const Orders = () => {
  // const [data, isLoading, _error, updateData] = useApi("/orders", [deleted]);
  const [tab, setTab] = useState(0);
  const ordersData = useSelector(getOrders);
  const dispatch = useDispatch();

  const handleSnack = useHandleSnack();
  const transactionData = useSelector(getTransactions); //useApi("/transactions");

  return (
    <Page>
      <Card>
        <Tabs
          value={tab}
          onChange={(_event, newValue) => {
            setTab(newValue);
          }}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Orders" />
          <Tab label="Transaction History" />
        </Tabs>
        {tab === 0 ? (
          <SortableStockTable
            columns={orderColumns}
            data={ordersData}
            key={"SortableStockTable-Orders"}
            handleDelete={({ id }) =>
              dispatch(removeFromOrdersWithSnack(id, handleSnack))
            }
          />
        ) : (
          <SortableStockTable
            columns={transactionsColumns}
            data={transactionData}
            key={"SortableStockTable-History"}
          />
        )}
      </Card>
    </Page>
  );
};

export default Orders;
