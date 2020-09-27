import React from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link } from "react-router-dom";

import { CenteredCard, CardHeading } from "../components/common/styled";
import app from "../utils/firebase";
import Page from "../components/page/Page";
import Login from "../components/login/LoginComponent";

import { useHistory } from "react-router-dom";

const LoginPage = () => {
  let history = useHistory();

  const SignIn = async (event) => {
    event.preventDefault();
    const { email, password } = event.target.elements;
    try {
      await app.auth().signInWithEmailAndPassword(email.value, password.value);
      history.push("/home");
    } catch (error) {
      alert(error);
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
    </Page>
  );
};

export default LoginPage;
