import React from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";

const Alert = ({ title, text, open, handleClose, isError }) => {
  return (
    <>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          <DialogContentText>{text}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>confirm</Button>
          {!isError && <Button onClick={handleClose}>cancel</Button>}
        </DialogActions>
      </Dialog>
    </>
  );
};
export default Alert;
