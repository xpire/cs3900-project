import React from "react";
import styled from "styled-components";

const CenteredDiv = styled.div`
  max-width: 1300px;
  margin: auto;
  padding: 10px;
`;
/**
 * Generic Page component with global page styles applied
 */
const Page = ({ children }) => {
  return <CenteredDiv>{children}</CenteredDiv>;
};

export default Page;
