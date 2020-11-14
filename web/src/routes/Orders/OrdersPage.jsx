import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import { tableTypes } from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";
import useApi from "../../hooks/useApi";
import useHandleSnack from "../../hooks/useHandleSnack";

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
        subtitleType={tableTypes.NUMBER}
      />
    ),
    align: "right",
  },
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

const Orders = () => {
  const [deleted, setDeleted] = useState(0);
  const [data, isLoading, _error, updateData] = useApi("/orders", [deleted]);
  const handleSnack = useHandleSnack();

  return (
    <Page>
      <Card>
        <SortableStockTable
          title="Limit Orders"
          columns={columns}
          data={data}
          isLoading={isLoading}
          handleDelete={({ id }) => {
            handleSnack(`/orders?id=${id}`, "delete").then(() => updateData());
          }}
          handleRefresh={() => updateData()}
        />
      </Card>
    </Page>
  );
};

export default Orders;
