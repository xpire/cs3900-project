import {
  Card,
  Typography,
  styled as materialStyled,
  Link,
} from "@material-ui/core";
import styled from "styled-components";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

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

export const BasicCard = materialStyled(Card)({
  margin: "10px",
});

export const StandardCard = materialStyled(BasicCard)({
  // padding: "10px",
  height: "95%",
});

export const InnerCard = materialStyled(BasicCard)({
  padding: "10px",
  height: "80%",
});

export const SubtitleLink = styled(Link)({
  marginTop: "10px",
});

export const StyledMarkdown = styled(ReactMarkdown)`
  blockquote {
    margin: 0;
    margin-top: 0;
    margin-bottom: 16px;
    padding: 0 15px;
    color: #777;
    border-left: 4px solid #ddd;
  }

  blockquote > :first-child {
    margin-top: 0;
  }

  blockquote > :last-child {
    margin-bottom: 0;
  }
`;
