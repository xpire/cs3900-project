import React, { useContext } from "react";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";

const Portfolio = () => {
  const { user } = useContext(AuthContext);
  return (
    <Page>
      <Card>
        <Typography variant="h2">Portfolio Page</Typography>
        <Typography>
          {`Welcome ${user.email} to the Portfolio page!`}
        </Typography>
      </Card>
    </Page>
  );
};

export default Portfolio;
