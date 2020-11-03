import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import { AuthContext } from "./authentication";
/**
 * Custom Private Route implementation which redirects to login page if user is unauthenticated
 */
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
