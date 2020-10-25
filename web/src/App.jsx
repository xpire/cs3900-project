import React, { useState } from "react";
import { Switch, useLocation, useHistory, Route } from "react-router-dom";
import { Button } from "@material-ui/core";
// import Hidden from "@material-ui/core/Hidden";

import { AuthProvider } from "./utils/authentication";
import { SnackbarProvider } from "notistack";
import Header from "./components/header/Header";
import Drawer from "./components/sidebar/SideBar";
import PrivateRoute from "./utils/PrivateRoute";
import { Routes } from "./utils/routes";
import AuthPage from "./routes/Auth/AuthPage";
import ScrollToTop from "./utils/scrollToTop";

function App() {
  const location = useLocation();
  const history = useHistory();

  const [isOpen, setOpen] = useState(false);
  const toggleDrawer = () => setOpen(!isOpen);

  const notistackRef = React.createRef();
  const onClickDismiss = (key) => () => {
    notistackRef.current.closeSnackbar(key);
  };
  return (
    <SnackbarProvider
      anchorOrigin={{
        vertical: "top",
        horizontal: "center",
      }}
      ref={notistackRef}
      action={(key) => <Button onClick={onClickDismiss(key)}>OK</Button>}
    >
      <AuthProvider>
        <ScrollToTop history={history}>
          <Header toggleMenu={toggleDrawer} />
          <Drawer
            isOpen={isOpen}
            handleChange={toggleDrawer}
            variant="temporary"
          />
          <Switch location={location} key={location.key}>
            <Route path="/auth" component={AuthPage} />
            {Routes.map(({ exact, path, isPublic, component }) => (
              <PrivateRoute
                exact={exact}
                path={path}
                isPublic={isPublic}
                component={component}
                key={path}
              />
            ))}
          </Switch>
        </ScrollToTop>
      </AuthProvider>
    </SnackbarProvider>
  );
}

export default App;
