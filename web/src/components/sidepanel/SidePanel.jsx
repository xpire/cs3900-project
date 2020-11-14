import React from "react";
import Drawer from "@material-ui/core/Drawer";
import { Toolbar } from "@material-ui/core";

function SidePanel({ classes, panel }) {
  /* CAN BE MADE INTO FLOATING, BY USING AN INTERNAL CARD*/
  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
      anchor="right"
    >
      <Toolbar />
      <div className={classes.drawerContainer}>
        <div style={{ padding: "20px" }}>{panel}</div>
      </div>
    </Drawer>
  );
}

export default SidePanel;
