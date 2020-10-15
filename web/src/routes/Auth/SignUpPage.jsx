import React, { useState } from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link } from "react-router-dom";

import { CenteredCard, CardHeading } from "../../components/common/styled";
import app, { ActionCodeSettings } from "../../utils/firebase";
import axios from "../../utils/api";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, { useAlert } from "../../components/common/Alert";

const SignUpPage = () => {
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [finished, setFinished] = useState(false);

  const SignUp = async (event) => {
    event.preventDefault();
    const { username, email, password, repeatPassword } = event.target.elements;
    try {
      if (repeatPassword.value !== password.value) {
        throw {
          code: "Passwords don't match!",
          message: "Please check that the password were entered in correctly.",
        };
      }
      await app
        .auth()
        .createUserWithEmailAndPassword(email.value, password.value);
      await app.auth().currentUser.sendEmailVerification(ActionCodeSettings);
      await axios.post(`/user?email=${email.value}&username=${username.value}`); //
      // history.push("/dashboard");
      setFinished(true);
    } catch (error) {
      createAlert(error);
    }
  };

  return (
    <Page>
      <CenteredCard>
        {finished ? (
          <CardHeading variant="h3">
            Please check your email to finish registration.
          </CardHeading>
        ) : (
          <>
            <CardHeading variant="h3">Sign Up</CardHeading>
            <Login
              buttonText="register"
              submitHandler={SignUp}
              repeat={true}
              username={true}
            />
            <MaterialLink to="/signin" component={Link} color="inherit">
              {"Already have an account? Sign in"}
            </MaterialLink>
          </>
        )}
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

export default SignUpPage;
