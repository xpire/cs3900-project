import React, { useContext } from "react";
import { Route, Redirect, useLocation, useHistory } from "react-router-dom";
import { AuthContext } from "./authentication";

// const handleResetPassword = ({ auth, actionCode, continueUrl }) => {
//   auth
//     .verifyPasswordResetCode(actionCode)
//     .then((email) => {
//       // do something with email
//       const newPassword = "";
//       auth
//         .confirmPasswordReset(actionCode, newPassword)
//         .then((resp) => {
//           // success
//         })
//         .catch((error) => {
//           // show error (code expired or weak password)
//         });
//     })
//     .catch((error) => {
//       // Ask user to try reset their password again (Invalid or expired action code)
//     });
// };

// const handleRecoverEmail = ({ auth, actionCode }) => {
//   var restoredEmail = null;
//   auth
//     .checkActionCode(actionCode)
//     .then(function(info) {
//       restoredEmail = info["data"]["email"];

//       // Revert to the old email.
//       return auth.applyActionCode(actionCode);
//     })
//     .then(function() {
//       // Account email reverted to restoredEmail

//       // TODO: Display a confirmation message to the user.

//       // You might also want to give the user the option to reset their password
//       // in case the account was compromised:
//       auth
//         .sendPasswordResetEmail(restoredEmail)
//         .then(function() {
//           // Password reset confirmation sent. Ask user to check their email.
//         })
//         .catch(function(error) {
//           // Error encountered while sending password reset code.
//         });
//     })
//     .catch(function(error) {
//       // Invalid code.
//     });
// };

// const handleVerifyEmail = ({ auth, actionCode, continueUrl }) => {
//   auth
//     .applyActionCode(actionCode)
//     .then(function(resp) {
//       // Email address has been verified.
//       // TODO: Display a confirmation message to the user.
//       history.push(continueUrl);
//     })
//     .catch(function(error) {
//       // Code is invalid or expired. Ask the user to verify their email address
//       // again.
//     });
// };

const PrivateRoute = ({ component: RouteComponent, isPublic, ...rest }) => {
  const { user } = useContext(AuthContext);
  // const location = useLocation();
  // const history = useHistory();
  // const getParameterByName = (s) => new URLSearchParams(location.search).get(s);

  // useEffect(() => {
  //   const mode = getParameterByName("mode");
  //   const actionCode = getParameterByName("oobCode");
  //   const continueUrl = getParameterByName("continueUrl");

  //   console.log({ mode, actionCode, continueUrl });

  //   switch (mode) {
  //     case "resetPassword":
  //       // Display reset password handler and UI.
  //       history.push("/resetPassword");
  //       handleResetPassword(auth, actionCode, continueUrl);
  //       break;
  //     case "recoverEmail":
  //       // Display email recovery handler and UI.
  //       history.push("/recoverEmail");
  //       handleRecoverEmail(auth, actionCode);
  //       break;
  //     case "verifyEmail":
  //       // Display email verification handler and UI.
  //       handleVerifyEmail(auth, actionCode, continueUrl);
  //       break;
  //     default:
  //     // Error: invalid mode.
  //   }
  // }, []);
  return (
    <Route
      {...rest}
      render={(routeProps) =>
        !!user || isPublic ? (
          <RouteComponent {...routeProps} />
        ) : (
          <Redirect to={"/signin"} />
        )
      }
    />
  );
};

export default PrivateRoute;
