import React from "react";
import { Typography, Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable from "../../components/common/SortableTable";

const Watchlist = () => {
  return (
    <Page>
      <Card>
        <SortableTable />
      </Card>
    </Page>
  );
};

export default Watchlist;
