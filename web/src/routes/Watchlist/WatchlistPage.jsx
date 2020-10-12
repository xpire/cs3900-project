import React, { useContext } from "react";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";

const Watchlist = () => {
  const { user } = useContext(AuthContext);
  return (
    <Page>
      <Card>
        <Typography variant="h2">Watchlist Page</Typography>
        <Typography>
          {`Welcome ${user.email} to the Watchlist page!`}
        </Typography>
      </Card>
    </Page>
  );
};

export default Watchlist;
