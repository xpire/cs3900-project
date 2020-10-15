import React from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link, useHistory } from "react-router-dom";

import { CenteredCard, CardHeading } from "../../components/common/styled";
import app from "../../utils/firebase";
import Page from "../../components/page/Page";
import Login from "../../components/login/LoginComponent";
import Alert, { useAlert } from "../../components/common/Alert";

const LoginPage = () => {
  let history = useHistory();
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();

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
        <CardHeading variant="h3">Sign In</CardHeading>
        <Login buttonText="login" submitHandler={SignIn} />
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

export default LoginPage;