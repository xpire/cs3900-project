import React, { useState, useEffect } from "react";
import { Link as MaterialLink, Typography } from "@material-ui/core";
import { Link, useLocation, useHistory } from "react-router-dom";
import styled from "styled-components";

import { CenteredCard, CardHeading } from "../components/common/styled";
import app from "../utils/firebase";
import Page from "../components/page/Page";
import Login from "../components/login/LoginComponent";
import Alert, { useAlert } from "../components/common/Alert";
import { getParameterByName } from "../utils/authentication";

export const CardBody = styled(Typography)`
  padding-bottom: 20px;
`;

const ResetPasswordPage = () => {
  let history = useHistory();
  const location = useLocation();
  const getParameterByName = (s) => new URLSearchParams(location.search).get(s);
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();

  useEffect(() => {
    // const mode = getParameterByName("mode");
    // const actionCode = getParameterByName("oobCode");
    // const continueUrl = getParameterByName("continueUrl");
    // console.log({ mode, actionCode, continueUrl });
    // if (mode !== "resetPassword") {
    //   // wrong mode
    //   createAlert("");
    // }
    // switch (mode) {
    //   case "resetPassword":
    //     // Display reset password handler and UI.
    //     history.push("/resetPassword");
    //     handleResetPassword(auth, actionCode, continueUrl);
    //     break;
    //   case "recoverEmail":
    //     // Display email recovery handler and UI.
    //     history.push("/recoverEmail");
    //     handleRecoverEmail(auth, actionCode);
    //     break;
    //   case "verifyEmail":
    //     // Display email verification handler and UI.
    //     handleVerifyEmail(auth, actionCode, continueUrl);
    //     break;
    //   default:
    //   // Error: invalid mode.
    // }
  }, []);

  const SignIn = async (event) => {
    event.preventDefault();
    const { email, password } = event.target.elements;
    try {
      await app.auth().signInWithEmailAndPassword(email.value, password.value);
      history.push("/home");
    } catch (error) {
      createAlert(error);
    }
  };
  return (
    <Page>
      <CenteredCard>
        <CardHeading variant="h3">Reset Password</CardHeading>
        <CardBody>Please enter your new password:</CardBody>
        <Login
          buttonText="login"
          submitHandler={SignIn}
          email={false}
          repeat={true}
        />
        <MaterialLink to="/signup" component={Link} color="inherit">
          {"Don't have an account? Sign up"}
        </MaterialLink>
      </CenteredCard>
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
