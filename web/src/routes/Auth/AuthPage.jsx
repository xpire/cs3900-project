import React, { useState } from "react";
import { Typography } from "@material-ui/core";
import { Link, useHistory, Redirect } from "react-router-dom";
import styled from "styled-components";
import { useSnackbar } from "notistack";

import {
  CenteredCard,
  CardHeading,
  SubtitleLink,
} from "../../components/common/styled";
import app, { useFirebaseAuth } from "../../utils/firebase";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, {
  useAlert,
  ValidationError,
} from "../../components/common/Alert";

export const CardBody = styled(Typography)`
  padding-bottom: 20px;
`;

const ResetPasswordPage = () => {
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [mode, actionCode /*, continueUrl*/] = useFirebaseAuth();
  const [loading, setLoading] = useState(false);
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
            enqueueSnackbar("Email has been Verified.", { variant: "success" });
            history.push("/");
          });
        break;
      default:
        throw new ValidationError(
          "Invalid URL",
          "The URL you tried to reach is invalid, please try again."
        );
      // Error: invalid mode.
    }
  } catch (error) {
    history.push("/");
    enqueueSnackbar(error.code, { variant: "error", preventDuplicate: true });
  }

  const ResetPassword = async (event) => {
    event.preventDefault();
    setLoading(true);
    const { password } = event.target.elements;
    try {
      await app.auth().confirmPasswordReset(actionCode, password.value);
      enqueueSnackbar("Password has been Reset.", { variant: "success" });
      history.push("/");
    } catch (error) {
      createAlert(error);
    } finally {
      setLoading(false);
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
            loading={loading}
          />
          <SubtitleLink to="/signup" component={Link} color="inherit">
            {"Don't have an account? Sign up"}
          </SubtitleLink>
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
        handleCancel={closeAlert}
        isError={true}
      />
    </Page>
  );
};

export default ResetPasswordPage;
