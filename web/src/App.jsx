import React, { useState } from "react";
import { Switch, useLocation, useHistory } from "react-router-dom";
import { CssBaseline } from "@material-ui/core";
// import Hidden from "@material-ui/core/Hidden";

import Header from "./components/header/Header";
import Drawer from "./components/sidebar/SideBar";
import PrivateRoute from "./utils/PrivateRoute";
import { Routes } from "./utils/routes";
import ScrollToTop from "./utils/scrollToTop";

function App() {
  const location = useLocation();
  const history = useHistory();

  const [isOpen, setOpen] = useState(false);
  const toggleDrawer = () => setOpen(!isOpen);

  return (
    <ScrollToTop history={history}>
      <Header toggleMenu={toggleDrawer} />
      <Drawer isOpen={isOpen} handleChange={toggleDrawer} variant="temporary" />
      <Switch location={location} key={location.key}>
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
  );
}

export default App;
