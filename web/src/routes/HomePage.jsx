import React from "react";
import { Typography, Card } from "@material-ui/core";

import Page from "../components/page/Page";

const Home = () => {
  return (
    <Page>
      <Card>
        <Typography variant="h2">Home Page</Typography>
        <Typography>Welcome to the home page!</Typography>
      </Card>
    </Page>
  );
};

export default Home;
