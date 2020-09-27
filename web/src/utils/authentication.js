import React from "react";
import app from "./firebase";
import {
  // Backdrop,
  CircularProgress,
} from "@material-ui/core";

import { useAuthState } from "react-firebase-hooks/auth";
// import { useCollectionData } from "react-firebase-hooks/firestore";

const auth = app.auth();
// const firestore = app.firestore();

export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [user, loading] = useAuthState(auth);
  if (loading) {
    return <CircularProgress color="primary" />; //Backdrop causes annoying dark flash
  }
  return (
    <AuthContext.Provider
      value={{
        user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
