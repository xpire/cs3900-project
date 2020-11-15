import React from "react";
import Drawer from "@material-ui/core/Drawer";
import { Toolbar, makeStyles } from "@material-ui/core";
import { DRAWER_WIDTH } from "../../constants/Layout";

const useStyles = makeStyles((theme) => ({
  drawer: {
    width: DRAWER_WIDTH,
    flexShrink: 0,
  },
  drawerPaper: {
    width: DRAWER_WIDTH,
    border: 0,
  },
  drawerContainer: {
    overflow: "hidden",
    padding: "15px",
  },
}));

function SidePanel({ panel }) {
  const classes = useStyles();

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
      <div className={classes.drawerContainer}>{panel}</div>
    </Drawer>
  );
}

export default SidePanel;
