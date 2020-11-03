import React, { useEffect, useState } from "react";
import { Card } from "@material-ui/core";

import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";

const headCells = [
  {
    id: "rank",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Rank",
  },
  {
    id: "username",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Name",
  },
  {
    id: "net_worth",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Net Worth",
  },
  {
    id: "level",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Level",
  },
];

const Leaderboard = () => {
  const [data, setData] = useState([]);
  useEffect(() => {
    axios
      .get("/leaderboard")
      .then((response) => {
        setData(
          response.data.rankings.map((elem, index) => {
            return { ...elem, rank: index + 1 };
          })
        );
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <Page>
      <Card>
        <SortableTable
          data={data}
          header={headCells}
          title="Leaderboard"
          buttons={false}
        />
      </Card>
    </Page>
  );
};

export default Leaderboard;
