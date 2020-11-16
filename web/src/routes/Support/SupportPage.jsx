import React, { useContext, useState } from "react";
import {
  Typography,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Button,
  CardContent,
  Chip,
  Grid,
  CardActionArea,
} from "@material-ui/core";
import app, { ActionCodeSettings } from "../../utils/firebase";
import { useSnackbar } from "notistack";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";
import useApi from "../../hooks/useApi";
import Alert, { useAlert } from "../../components/common/Alert";
import useHandleSnack from "../../hooks/useHandleSnack";
import TutorialDialog, { tutorials } from "../../tutorial/TutorialDialog";
import { useDispatch, useSelector } from "react-redux";
import { reloadAll } from "../../reducers";

const Support = () => {
  const { user } = useContext(AuthContext);
  const [forgotAlert, setForgotAlert] = useState(false);
  const [restartAlert, setRestartAlert] = useState(false);
  const [showAlert, alertDetails, createAlert, closeAlert] = useAlert();
  const { enqueueSnackbar } = useSnackbar();
  const handleSnack = useHandleSnack();

  const data = useSelector((state) => state.user.basic);
  const dispatch = useDispatch();

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
    handleSnack(`/user/reset`, "get").then(() => {
      setRestartAlert(false);
      dispatch(reloadAll);
    });
  };

  const [locked, lockedLoading] = useApi(`/user`, []); // check if functionality is locked
  const [chosen, setChosen] = useState({});
  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
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

      <Typography variant="h3">Tutorials</Typography>
      <Grid container>
        {tutorials.map((tut) => {
          return (
            <Grid md={4} sm={6} xs={12} key={tut.title}>
              <StandardCard>
                <CardActionArea
                  disabled={lockedLoading ? true : locked.level < tut.unlock}
                  onClick={() => {
                    console.log(tut);
                    setChosen(tut);
                    setOpen(true);
                  }}
                >
                  <CardContent>
                    <Typography variant="h5">{tut.title}</Typography>
                    <Chip
                      label={`Lv. ${tut.unlock}`}
                      color={
                        lockedLoading
                          ? "default"
                          : locked.level < tut.unlock
                          ? "default"
                          : "primary"
                      }
                    />
                  </CardContent>
                </CardActionArea>
              </StandardCard>
            </Grid>
          );
        })}
      </Grid>
      <TutorialDialog
        open={open}
        title={chosen.title}
        body={chosen.body}
        handleClose={handleClose}
      />

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
