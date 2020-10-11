import React from "react";
import {
  Card,
  Typography,
  styled as materialStyled,
  useTheme,
} from "@material-ui/core";
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

const StyledColoredText = materialStyled(Typography)({
  color: (props) => props.color,
});

export const green = { dark: "#c1ff7a", light: "#689f38" };
export const red = { dark: "#ef5350", light: "#f50057" };

export const ColoredText = ({ children, color, ...restProps }) => {
  const theme = useTheme();
  return (
    <StyledColoredText
      color={
        color === "green" ? green[theme.palette.type] : red[theme.palette.type]
      }
      {...restProps}
    >
      {children}
    </StyledColoredText>
  );
};

export const StandardCard = materialStyled(Card)({
  margin: "10px",
  padding: "10px",
  height: "95%",
});

export const InnerCard = materialStyled(Card)({
  margin: "10px",
  padding: "10px",
  height: "80%",
});
