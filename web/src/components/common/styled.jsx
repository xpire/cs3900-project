import { Card, Typography } from "@material-ui/core";
import styled from "styled-components";

export const CenteredCard = styled(Card)`
  width: min(90vw, 500px);
  margin: 20px auto;
  padding: 20px;
`;

export const CardHeading = styled(Typography)`
  padding: 20px 0;
`;
