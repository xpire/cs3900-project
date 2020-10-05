import React, { useContext } from "react";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";

const Trading = () => {
  const { user } = useContext(AuthContext);
  return (
    <Page>
      <Card>
        <Typography variant="h2">Trading Page</Typography>
        <Typography>{`Welcome ${user.email} to the Trading page!`}</Typography>
      </Card>
    </Page>
  );
};

export default Trading;
