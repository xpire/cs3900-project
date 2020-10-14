import React from "react";
import { Link as MaterialLink, Typography } from "@material-ui/core";
import { Link, useHistory, Redirect } from "react-router-dom";
import styled from "styled-components";
import { useSnackbar } from "notistack";

import { CenteredCard, CardHeading } from "../../components/common/styled";
import app, { useFirebaseAuth } from "../../utils/firebase";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, { useAlert } from "../../components/common/Alert";

export const CardBody = styled(Typography)`
  padding-bottom: 20px;
`;

const ResetPasswordPage = () => {
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [mode, actionCode, continueUrl] = useFirebaseAuth();
  const { enqueueSnackbar } = useSnackbar();
  let history = useHistory();

  try {
    switch (mode) {
      case "resetPassword":
        // Display reset password handler and UI.
        app.auth().verifyPasswordResetCode(actionCode);
        break;
      // case "recoverEmail":
      //   // Display email recovery handler and UI.
      //   handleRecoverEmail(auth, actionCode);
      //   break;
      case "verifyEmail":
        // Display email verification handler and UI.
        app
          .auth()
          .applyActionCode(actionCode)
          .then((resp) => {
            enqueueSnackbar("Email has been Verified.", { variant: "Success" });
            history.push("/");
          });
        break;
      default:
        throw { code: "Invalid URL" };
      // Error: invalid mode.
    }
  } catch (error) {
    history.push("/");
    console.log({ error });
    enqueueSnackbar(error.code, { variant: "Error", preventDuplicate: true });
  }

  const ResetPassword = async (event) => {
    event.preventDefault();
    const { password } = event.target.elements;
    console.log({ password });
    try {
      await app.auth().confirmPasswordReset(actionCode, password.value);
      enqueueSnackbar("Password has been Reset.", { variant: "Success" });
      history.push("/");
    } catch (error) {
      createAlert(error);
      console.log(error);
    }
  };

  return (
    <Page>
      {mode === "resetPassword" ? (
        <CenteredCard>
          <CardHeading variant="h3">Reset Password</CardHeading>
          <CardBody>Please enter your new password:</CardBody>
          <Login
            buttonText="login"
            submitHandler={ResetPassword}
            email={false}
            repeat={true}
          />
          <MaterialLink to="/signup" component={Link} color="inherit">
            {"Don't have an account? Sign up"}
          </MaterialLink>
        </CenteredCard>
      ) : mode === "verifyEmail" ? (
        <CenteredCard>
          <CardHeading variant="h3">Verifying Email...</CardHeading>
        </CenteredCard>
      ) : (
        <Redirect to="/" />
      )}
      <Alert
        title={alertDetails.code}
        text={alertDetails.message}
        open={showAlert}
        handleClose={closeAlert}
        isError={true}
      />
    </Page>
  );
};

export default ResetPasswordPage;
