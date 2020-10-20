import React, { useEffect, useState } from "react";
import app from "./firebase";
import { Typography, CircularProgress, useTheme } from "@material-ui/core";
import { motion, AnimatePresence } from "framer-motion";
import { useAuthState } from "react-firebase-hooks/auth";
import styled from "styled-components";

import axios from "./api";
import { CenteredMotionDiv } from "../components/common/styled";
const StyledCenteredMotionDiv = styled(CenteredMotionDiv)({
  background: (props) => props.theme.palette.background.default || "#303030",
});

const auth = app.auth();

export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [user, loading] = useAuthState(auth);
  const theme = useTheme();
  useEffect(() => {
    user &&
      user
        .getIdToken()
        .then((token) => {
          axios.defaults.headers.common["id-token"] = token;
        })
        .catch((e) => {
          delete axios.defaults.headers.common["id-token"];
        });
  }, [user]);
  return (
    <div style={{ background: theme.palette.background.default }}>
      <AnimatePresence exitBeforeEnter>
        {loading && (
          <StyledCenteredMotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ ease: "easeOut" }}
            key="validation"
            theme={theme}
            style={{ padding: "10px" }}
          >
            <Typography variant="h2">{"Validating your Session..."}</Typography>
            <CircularProgress color="primary" size={50} />
          </StyledCenteredMotionDiv>
        )}
        {!loading && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ease: "easeOut" }}
            key="application"
          >
            <AuthContext.Provider
              value={{
                user,
              }}
            >
              {children}
            </AuthContext.Provider>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
