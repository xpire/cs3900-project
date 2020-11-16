import React, { useEffect, useState } from "react";
import { Card } from "@material-ui/core";

import SortableStockTable, {
  tableTypes,
  RenderItem,
} from "../../components/common/SortableStockTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";
import { useSelector } from "react-redux";

const columns = [
  {
    field: "rank",
    title: <RenderItem title="Rank" alignItems="flex-start" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.rank}
        titleType={tableTypes.NUMBER}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "username",
    title: <RenderItem title="Username" subtitle="Level" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.username}
        titleType={tableTypes.TEXT}
        subtitle={`Lv. ${rowData.level}`}
        subtitleType={tableTypes.TEXT}
      />
    ),
    align: "right",
  },
  {
    field: "net_worth",
    title: <RenderItem title="Net Worth" />,
    render: (rowData) => (
      <RenderItem title={rowData.net_worth} titleType={tableTypes.CURRENCY} />
    ),
    align: "right",
  },
];

const Leaderboard = () => {
  const isLoading = useSelector((state) => state.user.is_loading);
  const { rankings, user_ranking } = useSelector(
    (state) => state.user.leaderboard
  );

  const data = rankings.map((elem, index) => ({ ...elem, rank: index + 1 }));
  return (
    <Page>
      <Card>
        <SortableStockTable
          title="Leaderboard"
          columns={columns}
          data={data}
          isLoading={isLoading}
          buttons={false}
        />
      </Card>
    </Page>
  );
};

export default Leaderboard;
