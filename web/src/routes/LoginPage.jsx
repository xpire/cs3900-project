import React, { useState } from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link, useHistory } from "react-router-dom";

import { CenteredCard, CardHeading } from "../components/common/styled";
import app from "../utils/firebase";
import Page from "../components/page/Page";
import Login from "../components/login/LoginComponent";
import Alert from "../components/common/Alert";

const LoginPage = () => {
  let history = useHistory();
  const [showAlert, setShowAlert] = useState(false);
  const [alertDetails, setAlertDetails] = useState({});

  const SignIn = async (event) => {
    event.preventDefault();
    const { email, password } = event.target.elements;
    try {
      await app.auth().signInWithEmailAndPassword(email.value, password.value);
      history.push("/home");
    } catch (error) {
      console.log({ error });
      setShowAlert(true);
      setAlertDetails(error);
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
        handleClose={() => setShowAlert(false)}
        isError={true}
      />
    </Page>
  );
};

export default LoginPage;
