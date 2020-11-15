import React from "react";
import Drawer from "@material-ui/core/Drawer";
import { Toolbar } from "@material-ui/core";
import styled from "styled-components";

const PaddedDiv = styled.div`
  padding: 20px;
`;

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
        <PaddedDiv>{panel}</PaddedDiv>
      </div>
    </Drawer>
  );
}

export default SidePanel;
