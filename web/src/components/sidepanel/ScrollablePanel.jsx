import { makeStyles } from "@material-ui/core";
import React from "react";
import { Scrollbars } from "react-custom-scrollbars";
import styled from "styled-components";

const useStyles = makeStyles((theme) => ({
  scrollableContainer: {
    overflowY: "auto",
    overflowX: "hidden",
    maxHeight: "100vh",
    marginRight: "-15px",
    paddingRight: "15px",
  },
}));

const StyledScrollbars = styled(Scrollbars)`
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 100vh;
  margin-right: -15px;
  padding-right: 15px;
`;

function ScrollPanel({ title, content, addPadding = true }) {
  const classes = useStyles();
  return (
    <div>
      {title}
      <StyledScrollbars style={{ height: "100vh" }}>
        {content}
        {addPadding ? <div style={{ height: "80vh" }}></div> : <></>}
      </StyledScrollbars>
    </div>
  );
}

export default ScrollPanel;
