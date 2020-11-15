import React, { useState } from "react";
import { TextField, Grid, Button, LinearProgress } from "@material-ui/core";
import { Link } from "react-router-dom";
import { useSnackbar } from "notistack";

import {
  CenteredCard,
  CardHeading,
  SubtitleLink,
} from "../../components/common/styled";
import app, { ActionCodeSettings } from "../../utils/firebase";
import Page from "../../components/page/Page";
import Alert, { useAlert } from "../../components/common/Alert";

const ForgotPasswordPage = () => {
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const { enqueueSnackbar } = useSnackbar();

  const ForgotPassword = async (event) => {
    event.preventDefault();
    setLoading(true);
    const { email } = event.target.elements;
    try {
      await app.auth().sendPasswordResetEmail(email.value, ActionCodeSettings);
      enqueueSnackbar("Reset Email has been sent.", { variant: "success" });
      setFinished(true);
      setLoading(false);
    } catch (error) {
      createAlert(error);
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
            <SubtitleLink to="/signin" component={Link} color="primary">
              {"Remember your password? Sign in"}
            </SubtitleLink>
          </>
        )}
      </CenteredCard>
      <Alert
        title={alertDetails.code}
        text={alertDetails.message}
        open={showAlert}
        handleClose={closeAlert}
        handleCancel={closeAlert}
        isError={true}
      />
    </Page>
  );
};

export default ForgotPasswordPage;
