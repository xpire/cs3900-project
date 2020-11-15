import React, { useEffect, useState } from "react";
import { Card } from "@material-ui/core";

import { tableTypes } from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";

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
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  const refreshTable = () => {
    setLoading(true);
    axios
      .get("/leaderboard")
      .then((response) => {
        setData(
          response.data.rankings.map((elem, index) => {
            return { ...elem, rank: index + 1 };
          })
        );
        setLoading(false);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    refreshTable();
  }, []);

  const handleRefresh = () => {
    refreshTable();
  };

  return (
    <Page>
      <Card>
        <SortableStockTable
          title="Leaderboard"
          columns={columns}
          data={data}
          isLoading={loading}
          buttons={false}
          handleRefresh={handleRefresh}
        />
      </Card>
    </Page>
  );
};

export default Leaderboard;
