import React from "react";
import app from "./firebase";
import { Typography, CircularProgress } from "@material-ui/core";
import { motion, AnimatePresence } from "framer-motion";
import { useAuthState } from "react-firebase-hooks/auth";

import { CenteredMotionDiv } from "../components/common/styled";

const auth = app.auth();

export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [user, loading] = useAuthState(auth);

  return (
    <div>
      <AnimatePresence exitBeforeEnter>
        {loading && (
          <CenteredMotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ ease: "easeOut" }}
            key="validation"
          >
            <Typography variant="h2">Validating your Session...</Typography>
            <CircularProgress color="primary" size={50} />
          </CenteredMotionDiv>
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
