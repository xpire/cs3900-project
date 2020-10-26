import React, { useState } from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";

const Alert = ({ title, text, open, handleClose, handleCancel, isError }) => {
  return (
    <>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          <DialogContentText>{text}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>OK</Button>
          {!isError && <Button onClick={handleCancel}>cancel</Button>}
        </DialogActions>
      </Dialog>
    </>
  );
};
export default Alert;

export const useAlert = () => {
  const [showAlert, setShowAlert] = useState(false);
  const [alertDetails, setAlertDetails] = useState({});

  const createAlert = (e) => {
    setAlertDetails(e);
    setShowAlert(true);
  };

  const closeAlert = () => setShowAlert(false);

  return [showAlert, alertDetails, createAlert, closeAlert];
};
