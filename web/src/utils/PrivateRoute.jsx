import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import { AuthContext } from "./authentication";

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

const PrivateRoute = ({ component: RouteComponent, isPublic, ...rest }) => {
  const { user } = useContext(AuthContext);
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
