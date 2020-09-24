import React from "react";
import { Typography, Card } from "@material-ui/core";

import Page from "../components/Page/Page";

const Login = () => {
  return (
    <Page>
      <Card>
        <Typography variant="h2">Login Page</Typography>
        <Typography>Welcome to the Login page!</Typography>
      </Card>
    </Page>
  );
};

export default Login;
