import React, { useEffect, useState } from "react";
import app from "./firebase";
import { useTheme } from "@material-ui/core";
import { motion, AnimatePresence } from "framer-motion";
import { useAuthState } from "react-firebase-hooks/auth";
import styled from "styled-components";
import useWindowSize from "react-use/lib/useWindowSize";
import Confetti from "react-confetti";
import Logo from "../logo.svg";
import { useDispatch } from "react-redux";

import axios from "./api";
import { CenteredMotionDiv } from "../components/common/styled";
import useSockets from "../hooks/useSockets";
import useHandleSocketSnack from "../hooks/useHandleSocketSnack";
import { initState } from "../reducers";
import * as rax from "retry-axios";

const StyledCenteredMotionDiv = styled(CenteredMotionDiv)({
  background: (props) => props.theme.palette.background.default || "#303030",
});

axios.defaults.raxConfig = {
  instance: axios,
};
const interceptorId = rax.attach(axios);

export const auth = app.auth();
export const AuthContext = React.createContext();

const updateAxiosUserToken = (user) => {
  user &&
    user
      .getIdToken()
      .then((token) => (axios.defaults.headers.common["id-token"] = token))
      .catch((e) => {});
};

/**
 * A Component which wraps the Application, and provides a visualisation for authentication
 */
export const AuthProvider = ({ children }) => {
  const [user, loading] = useAuthState(auth);
  const theme = useTheme();

  // for redux data management
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(initState());
  }, []);

  useEffect(() => {
    updateAxiosUserToken(user);
    axios.defaults.raxConfig = {
      statusCodesToRetry: [[400, 402]],
      onRetryAttempt: (err) => {
        const cfg = rax.getConfig(err);
        console.log(`Retry attempt #${cfg.currentRetryAttempt}`);
        console.log("REFRESH TOKEN!");
        return updateAxiosUserToken(user);
      },
    };
  }, [user, loading]);

  const [celebration, setCelebration] = useState(false);
  const handleSnack = useHandleSocketSnack(setCelebration);

  const [lastJsonMessage] = useSockets();
  useEffect(() => {
    handleSnack(lastJsonMessage);
  }, [lastJsonMessage]);

  const { width, height } = useWindowSize();
  return (
    <div style={{ background: theme.palette.background.default }}>
      <AnimatePresence exitBeforeEnter>
        {loading && (
          <StyledCenteredMotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: 0 }}
            transition={{ ease: "easeOut" }}
            key="validation"
            theme={theme}
          >
            <motion.img
              src={Logo}
              alt="X"
              height="150px"
              initial={{ scale: 0.85, opacity: 0.8 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{
                duration: 1,
                repeat: Infinity,
                repeatType: "mirror",
                ease: "easeOut",
                // repeatDelay: 0.1,
              }}
            />
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
              {celebration && (
                <Confetti
                  width={width}
                  height={height}
                  numberOfPieces={200}
                  recycle={false}
                  gravity={0.1}
                  onConfettiComplete={() => setCelebration(false)}
                />
              )}
            </AuthContext.Provider>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
