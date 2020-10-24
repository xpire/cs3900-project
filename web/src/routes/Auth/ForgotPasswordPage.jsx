import React, { useState } from "react";
import {
  Link as MaterialLink,
  TextField,
  Grid,
  Button,
  LinearProgress,
} from "@material-ui/core";
import { Link } from "react-router-dom";

import { CenteredCard, CardHeading } from "../../components/common/styled";
import app, { ActionCodeSettings } from "../../utils/firebase";
import Page from "../../components/page/Page";

const ForgotPasswordPage = () => {
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(false);

  const ForgotPassword = async (event) => {
    event.preventDefault();
    setLoading(true);
    const { email } = event.target.elements;
    try {
      await app.auth().sendPasswordResetEmail(email.value, ActionCodeSettings);
      setFinished(true);
      setLoading(false);
    } catch (error) {
      alert(error);
      setLoading(false);
    }
  };

  return (
    <Page>
      <CenteredCard>
        {finished ? (
          <CardHeading variant="h3">
            Please check your email to reset your password
          </CardHeading>
        ) : (
          <>
            <CardHeading variant="h3">Forgot password?</CardHeading>
            <form onSubmit={ForgotPassword}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    name="email"
                    variant="outlined"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    type="email"
                    autoFocus
                  />
                </Grid>
                <Grid item xs={12}>
                  {loading && <LinearProgress />}
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    disabled={loading}
                  >
                    Submit
                  </Button>
                </Grid>
              </Grid>
            </form>
            <MaterialLink to="/signin" component={Link} color="inherit">
              {"Remember your password? Sign in"}
            </MaterialLink>
          </>
        )}
      </CenteredCard>
    </Page>
  );
};

export default ForgotPasswordPage;
