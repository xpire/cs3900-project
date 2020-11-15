import { makeStyles } from "@material-ui/core";
import React from "react";

const useStyles = makeStyles((theme) => ({
  scrollableContainer: {
    overflow: "scroll",
    maxHeight: "100vh",
    marginRight: "-15px",
    paddingRight: "15px",
  },
}));

function ScrollPanel({ title, content, addPadding = true }) {
  const classes = useStyles();
  return (
    <div>
      {title}
      <div className={classes.scrollableContainer}>
        {content}
        {addPadding ? <div style={{ height: "80vh" }}></div> : <></>}
      </div>
    </div>
  );
}

export default ScrollPanel;
