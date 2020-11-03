import React, { useState } from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import useApi from "../../hooks/useApi";
import useHandleSnack from "../../hooks/useHandleSnack";

const headCells = [
  {
    id: "id",
    formatType: tableTypes.ID,
    disablePadding: false,
    label: "Id",
  },
  {
    id: "symbol",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Symbol",
  },
  {
    id: "name",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Name",
  },
  {
    id: "exchange",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Exchange",
  },
  {
    id: "type",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Type",
  },
  {
    id: "qty",
    formatType: tableTypes.NUMBER,
    disablePadding: false,
    label: "Quantity",
  },
  {
    id: "limit_price",
    formatType: tableTypes.CURRENCY,
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
          title="Limit Orders"
          handleDelete={({ id }) => {
            handleSnack(`/orders?id=${id}`, "delete").then(() =>
              setDeleted(deleted + 1)
            );
          }}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
