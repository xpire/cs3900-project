import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import { AuthContext } from "./authentication";
import app from "./firebase";

/**
 * Custom Private Route implementation which redirects to login page if user is unauthenticated
 */
const PrivateRoute = ({ component: RouteComponent, isPublic, ...rest }) => {
  const { user } = useContext(AuthContext);

  // if (!! user && ! user.emailVerified) {
  //   history.push("/signin")
  // }

  if ((!! user && user.emailVerified) || isPublic) {
    return (
      <Route
      {...rest}
      render={(routeProps) => <RouteComponent {...routeProps} />}
      />
    )
  } else {
    if (!! user){ 
      app.auth().signOut()
      return (
        <Route
          {...rest}
          render= {(routeProps) => (<Redirect to="/signin" />)}
        />
      )
    } else {
      
    }
  }

  // return (
  //   <Route
  //     {...rest}
  //     render={(routeProps) =>
  //       !!user || isPublic ? (
  //         <RouteComponent {...routeProps} />
  //       ) : (
  //         <Redirect to={"/signin"} />
  //       )
  //     }
  //   />
  // );
};

export default PrivateRoute;
