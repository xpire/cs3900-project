import React, { useState } from "react";
import { Link as MaterialLink } from "@material-ui/core";
import { Link } from "react-router-dom";

import { CenteredCard, CardHeading } from "../components/common/styled";
import app from "../utils/firebase";
import Page from "../components/page/Page";
import Login from "../components/login/LoginComponent";
import { useHistory } from "react-router-dom";
import Alert, { useAlert } from "../components/common/Alert";

const SignUpPage = () => {
  let history = useHistory();
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const [finished, setFinished] = useState(false);

  const SignUp = async (event) => {
    event.preventDefault();
    const { email, password, repeatPassword } = event.target.elements;
    try {
      console.log(
        [email, password, repeatPassword].map((e) => console.log(e.value))
      );
      if (repeatPassword.value !== password.value) {
        throw {
          code: "Passwords don't match!",
          message: "Please check that the password were entered in correctly.",
        };
      }
      await app
        .auth()
        .createUserWithEmailAndPassword(email.value, password.value);
      history.push("/dashboard");
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
            <Login buttonText="register" submitHandler={SignUp} repeat={true} />
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
