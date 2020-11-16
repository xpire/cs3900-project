import React, { useState } from "react";
import { Link } from "react-router-dom";

import {
  CenteredCard,
  CardHeading,
  SubtitleLink,
} from "../../components/common/styled";
import app, { ActionCodeSettings } from "../../utils/firebase";
import axios from "../../utils/api";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, {
  useAlert,
  ValidationError,
} from "../../components/common/Alert";

const SignUpPage = () => {
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(false);

  const SignUp = async (event) => {
    event.preventDefault();
    const { username, email, password, repeatPassword } = event.target.elements;
    try {
      setLoading(true);
      if (repeatPassword.value !== password.value) {
        throw new ValidationError(
          "Passwords don't match!",
          "Please check that the password were entered in correctly."
        );
      }
      await app
        .auth()
        .createUserWithEmailAndPassword(email.value, password.value);
      await app.auth().currentUser.sendEmailVerification(ActionCodeSettings);
      await axios.post(`/user?email=${email.value}&username=${username.value}`); //
      app.auth().signOut();

      // history.push("/dashboard");
      setFinished(true);
    } catch (error) {
      createAlert(error);
    } finally {
      setLoading(false);
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
              buttonText="Sign Up"
              submitHandler={SignUp}
              repeat={true}
              username={true}
              loading={loading}
            />
            <SubtitleLink to="/signin" component={Link}>
              {"Already have an account? Sign in"}
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

export default SignUpPage;
