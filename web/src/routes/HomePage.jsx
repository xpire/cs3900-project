import React from "react";
import { Typography, Link as MaterialLink } from "@material-ui/core";
import { Link } from "react-router-dom";

import Page from "../components/page/Page";
import { CenteredCard } from "../components/common/styled";

const Home = () => {
  return (
    <Page>
      <CenteredCard>
        <Typography variant="h2">Execute the Deal</Typography>
        <Typography variant="subtitle2">Investment Simulator</Typography>
        <Typography>Want to learn how to trade?</Typography>
        <MaterialLink component={Link} to="/signup">
          Sign Up now.
        </MaterialLink>
      </CenteredCard>
    </Page>
  );
};

export default Home;
