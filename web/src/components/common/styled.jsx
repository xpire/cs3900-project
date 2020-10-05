import { Card, Typography } from "@material-ui/core";
import styled from "styled-components";
import { motion } from "framer-motion";

export const CenteredCard = styled(Card)`
  width: min(90vw, 500px);
  margin: 20px auto;
  padding: 20px;
`;

export const CardHeading = styled(Typography)`
  padding: 20px 0;
`;

export const CenteredMotionDiv = styled(motion.div)`
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
`;
