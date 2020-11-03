import React, { useState } from "react";
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
  const [loading, setLoading] = useState(false);

  const SignIn = async (event) => {
    event.preventDefault();
    setLoading(true);
    const { email, password } = event.target.elements;
    try {
      await app.auth().signInWithEmailAndPassword(email.value, password.value);
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
        <MaterialLink to="/signup" component={Link} color="inherit">
          {" "}
          {
            //TODO make it blue and more spacing
          }
          {"Don't have an account? Sign up"}
        </MaterialLink>
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
