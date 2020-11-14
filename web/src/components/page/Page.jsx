import { Hidden } from "@material-ui/core";
import React from "react";
import styled from "styled-components";

const CenteredDiv = styled.div`
  max-width: 1200px;
  margin: auto;
  padding: 10px;
  overflow: auto;
`;
/**
 * Generic Page component with global page styles applied
 */
const Page = ({ children }) => {
  return (
    <div>
      <Hidden mdUp>
        <CenteredDiv style={{ width: "100vw" }}>{children}</CenteredDiv>
      </Hidden>
      <Hidden smDown>
        <CenteredDiv style={{ width: `calc(100vw - 380px)` }}>
          {children}
        </CenteredDiv>
      </Hidden>
    </div>
  );
};

export default Page;
