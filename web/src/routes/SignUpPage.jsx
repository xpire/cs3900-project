import React from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link } from "react-router-dom";

import { CenteredCard, CardHeading } from "../components/common/styled";
import app from "../utils/firebase";
import Page from "../components/page/Page";
import Login from "../components/login/LoginComponent";
import { useHistory } from "react-router-dom";

const SignUpPage = () => {
  let history = useHistory();

  const SignUp = async (event) => {
    event.preventDefault();
    const { email, password } = event.target.elements;
    try {
      await app
        .auth()
        .createUserWithEmailAndPassword(email.value, password.value);
      history.push("/dashboard");
    } catch (error) {
      alert(error);
    }
  };

  return (
    <Page>
      <CenteredCard>
        <CardHeading variant="h3">Sign Up</CardHeading>
        <Login buttonText="register" submitHandler={SignUp} />
        <MaterialLink to="/signin" component={Link} color="inherit">
          {"Already have an account? Sign in"}
        </MaterialLink>
      </CenteredCard>
    </Page>
  );
};

export default SignUpPage;
