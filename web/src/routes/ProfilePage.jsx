import React, { useContext } from "react";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";

const Profile = () => {
  const { user } = useContext(AuthContext);
  return (
    <Page>
      <Card>
        <Typography variant="h2">Profile Page</Typography>
        <Typography>{`Welcome ${user.email} to the Profile page!`}</Typography>
      </Card>
    </Page>
  );
};

export default Profile;
