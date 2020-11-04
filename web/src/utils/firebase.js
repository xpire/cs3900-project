import * as firebase from "firebase/app";
import "firebase/auth";
import { useLocation } from "react-router-dom";

/**
 * frontend firebase configs
 */
const app = firebase.initializeApp({
  apiKey: "AIzaSyAtmPkkkMW6osBz79xGXsC50vQ_NoBpCYM",
  authDomain: "ecksdee-132d1.firebaseapp.com",
  databaseURL: "https://ecksdee-132d1.firebaseio.com",
  projectId: "ecksdee-132d1",
  storageBucket: "ecksdee-132d1.appspot.com",
  messagingSenderId: "653502353731",
  appId: "1:653502353731:web:29b2f35630fbb346eb5ff6",
});

export default app;
// thanks https://www.wrappixel.com/react-firebase-authentication/

/**
 * Default ActionCodeSettings for use with firebase password reset and email verification methods
 */
export const ActionCodeSettings = {
  url: `http://localhost:${
    process.env.NODE_ENV === "development" ? 3000 : 5000
  }/home`,
  handleCodeInApp: true,
};

/**
 * A React Hook to simplify parsing of url search parameters for password reset and email verification methods
 */
export const useFirebaseAuth = () => {
  const location = useLocation();
  const getParameterByName = (s) => new URLSearchParams(location.search).get(s);
  const mode = getParameterByName("mode");
  const actionCode = getParameterByName("oobCode");
  const continueUrl = getParameterByName("continueUrl");
  return [mode, actionCode, continueUrl];
};
