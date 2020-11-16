import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";

import {
  CenteredCard,
  CardHeading,
  SubtitleLink,
} from "../../components/common/styled";
import app from "../../utils/firebase";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, {
  useAlert,
  ValidationError,
} from "../../components/common/Alert";

const LoginPage = () => {
  let history = useHistory();
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [loading, setLoading] = useState(false);

  const SignIn = async (event) => {
    event.preventDefault();
    setLoading(true);
    const { email, password } = event.target.elements;
    try {
      await app
        .auth()
        .signInWithEmailAndPassword(email.value, password.value)
        .then((authUser) => {
          if (!authUser.user.emailVerified) {
            app.auth().signOut();
            throw new ValidationError(
              "Email not Verified",
              "Please check your email and click the email verification link to continue using this application."
            );
          }
        });
      history.push("/home");
    } catch (error) {
      createAlert(error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Page>
      <CenteredCard>
        <CardHeading variant="h3">Sign In</CardHeading>
        <Login buttonText="login" submitHandler={SignIn} loading={loading} />
        <SubtitleLink to="/signup" component={Link}>
          {"Don't have an account? Sign up"}
        </SubtitleLink>
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

export default LoginPage;
