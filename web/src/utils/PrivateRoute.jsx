import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import { AuthContext } from "./authentication";

const PrivateRoute = ({ component: RouteComponent, isPublic, ...rest }) => {
  const { user } = useContext(AuthContext);
  console.log(user && user.email);
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
