import React, { useEffect, useState } from "react";
import app from "./firebase";
import { Typography, CircularProgress, useTheme } from "@material-ui/core";
import { motion, AnimatePresence } from "framer-motion";
import { useAuthState } from "react-firebase-hooks/auth";
import styled from "styled-components";
import { useSnackbar } from "notistack";

import axios from "./api";
import { CenteredMotionDiv } from "../components/common/styled";
import useSockets from "../hooks/useSockets";
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

  const { enqueueSnackbar } = useSnackbar();
  const [lastJsonMessage, messageHistory, connectionStatus] = useSockets();
  useEffect(() => {
    switch (lastJsonMessage?.type) {
      case "auth":
        enqueueSnackbar(`${lastJsonMessage?.msg}`, {
          variant: "info",
        });
        break;
      case "notif":
        if (lastJsonMessage.msg.event_type === `LEVEL_UP`) {
          enqueueSnackbar(`Level Up! Lv. ${lastJsonMessage.msg.new_level}`, {
            variant: "success",
          });
        } else if (lastJsonMessage.msg.event_type === `ACHIEVEMENT_UNLOCKED`) {
          enqueueSnackbar(
            `Achievement Unlocked! ${JSON.stringify(lastJsonMessage.msg)}`,
            {
              variant: "success",
            }
          );
        } else {
          enqueueSnackbar(`${JSON.stringify(lastJsonMessage)}`, {
            variant: "success",
          });
        }
        break;
      default:
    }
  }, [lastJsonMessage]);
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
