import React, { useState } from "react";
import PropTypes from "prop-types";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";

/**
 * A component that shows a material-ui Dialog box when an Alert/Warning requiring User acknowledgement is shown
 */
const Alert = ({ title, text, open, handleClose, handleCancel, isError }) => {
  return (
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
  );
};

Alert.propTypes = {
  /** The title text shown in the Alert */
  title: PropTypes.string,
  /** The subtitle text shown in the Alert */
  text: PropTypes.string,
  /** Whether the Alert Dialog is open, should be controlled with a react useState. */
  open: PropTypes.bool,
  /** A function that runs when the OK button is clicked */
  handleClose: PropTypes.func,
  /** A function that runs when the cancel button is clicked */
  handleCancel: PropTypes.func,
  /** Whether the Alert is for an error (if soo, don't show a cancel button) */
  isError: PropTypes.bool,
};

export default Alert;
/**
 * A react hook for use with Alert component.
 * The usage is as follows:
 * ```<Alert
        title={alertDetails.code}
        text={alertDetails.message}
        open={showAlert}
        handleClose={closeAlert}
      />
 * ```
 * When you have an error / message to show, you would set it like `createAlert({code: "title", message: "subtitle"});`
 */

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

export class ValidationError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "ValidationError";
    this.code = code;
  }
}
