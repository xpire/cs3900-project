import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";
import useApi from "../../hooks/useApi";
import useHandleSnack from "../../hooks/useHandleSnack";

const headCells = [
  { id: "id", numeric: false, disablePadding: false, label: "Id" },
  { id: "symbol", numeric: false, disablePadding: false, label: "Symbol" },
  { id: "name", numeric: false, disablePadding: false, label: "Name" },
  { id: "exchange", numeric: false, disablePadding: false, label: "Exchange" },
  { id: "type", numeric: false, disablePadding: false, label: "Type" },
  { id: "quantity", numeric: true, disablePadding: false, label: "Quantity" },
  {
    id: "price",
    numeric: true,
    disablePadding: false,
    label: "Price",
    color: true,
  },
];

const Watchlist = () => {
  const [deleted, setDeleted] = useState(0);
  const [data, loading] = useApi("/orders", [deleted]);
  const handleSnack = useHandleSnack();

  return (
    <Page>
      <Card>
        <SortableTable
          data={data}
          header={headCells}
          title="Watch List"
          handleDelete={({ id }) => {
            handleSnack(`/orders?identity=${id}`, "delete").then(() =>
              setDeleted(deleted + 1)
            );
          }}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
