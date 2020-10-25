import React, { useContext, useState } from "react";
import {
  Typography,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Button,
  CardContent,
} from "@material-ui/core";
import app, { ActionCodeSettings } from "../../utils/firebase";
import { useSnackbar } from "notistack";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import Alert, { useAlert } from "../../components/common/Alert";
import useHandleSnack from "../../hooks/useHandleSnack";

const Support = () => {
  const { user } = useContext(AuthContext);
  const [data] = useApi("/user");
  const [forgotAlert, setForgotAlert] = useState(false);
  const [restartAlert, setRestartAlert] = useState(false);
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const { enqueueSnackbar } = useSnackbar();
  const handleSnack = useHandleSnack();

  const handleForgotPassword = async () => {
    try {
      await app
        .auth()
        .sendPasswordResetEmail(user.email, ActionCodeSettings)
        .then(() =>
          enqueueSnackbar("Reset Email has been sent.", { variant: "success" })
        )
        .catch(() =>
          enqueueSnackbar("Error occurred. Please try again", {
            variant: "error",
          })
        );
      await app.auth().signOut();
    } catch (error) {
      createAlert(error);
    }
    setForgotAlert(false);
  };
  const handleRestartGame = () => {
    alert("hit the reset api"); //TODO: use handleSnack to handle restartGame API
    // handleSnack(`/reset`, "post")
    fetch("/this doesnt exist")
      .catch()
      .then(() => {
        setRestartAlert(false);
      });
  };
  return (
    <Page>
      <StandardCard>
        <CardContent>
          <Typography variant="h3">General Account Details</Typography>
        </CardContent>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Username</TableCell>
              <TableCell align="right">{data.username} </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Email</TableCell>
              <TableCell align="right">{user.email} </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Forgot Password?</TableCell>
              <TableCell align="right">
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setForgotAlert(true)}
                >
                  Reset Password
                </Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Restart Game</TableCell>
              <TableCell align="right">
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setRestartAlert(true)}
                >
                  Restart
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </StandardCard>
      <StandardCard>
        <CardContent>
          <Typography variant="h3">Tutorials</Typography>
        </CardContent>
      </StandardCard>
      <Alert
        title="Are you sure?"
        text="You will be logged out and receive an email giving you instructions on how to reset your password"
        open={forgotAlert}
        handleClose={handleForgotPassword}
        handleCancel={() => setForgotAlert(false)}
        isError={false}
      />
      <Alert
        title="Are you sure?"
        text="You will lose your current balance, all transaction history and other user information, and be given the starting balance."
        open={restartAlert}
        handleClose={handleRestartGame}
        handleCancel={() => setRestartAlert(false)}
        isError={false}
      />
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

export default Support;
