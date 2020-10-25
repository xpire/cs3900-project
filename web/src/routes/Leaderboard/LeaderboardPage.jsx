import React, { useContext, useEffect, useState } from "react";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../../utils/authentication";
import SortableTable from "../../components/common/SortableTable";
import Page from "../../components/page/Page";
import axios from "../../utils/api";

const headCells = [
  { id: "rank", numeric: false, disablePadding: false, label: "Rank" },
  { id: "username", numeric: false, disablePadding: false, label: "Name" },
  {
    id: "net_worth",
    numeric: true,
    disablePadding: false,
    label: "Net Worth",
  },
  {
    id: "level",
    numeric: true,
    disablePadding: false,
    label: "Level",
  },
];

const Leaderboard = () => {
  const { user } = useContext(AuthContext);
  const [data, setData] = useState([]);
  useEffect(() => {
    axios
      .get("/leaderboard")
      .then((response) => {
        console.log({ response });
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
