import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import { AuthContext } from "./authentication";
/**
 * Custom Private Route implementation which redirects to login page if user is unauthenticated
 */
const PrivateRoute = ({ component: RouteComponent, isPublic, ...rest }) => {
  const { user } = useContext(AuthContext);
  console.log(user?.emailVerified);
  return (
    <Route
      {...rest}
      render={(routeProps) =>
        !!user || !user?.emailVerified || isPublic ? (
          <RouteComponent {...routeProps} />
        ) : (
          <Redirect to={"/signin"} />
        )
      }
    />
  );
};

export default PrivateRoute;
