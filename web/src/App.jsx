import React, { useState } from "react";
import { Switch, useLocation } from "react-router-dom";
// import Hidden from "@material-ui/core/Hidden";

import ThemeProvider from "./utils/ThemeProvider";
import Header from "./components/header/Header";
import Drawer from "./components/sidebar/SideBar";
import PrivateRoute from "./utils/PrivateRoute";
import { Routes } from "./utils/routes";

function App() {
  const location = useLocation();

  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => setDarkMode(!darkMode);

  const [isOpen, setOpen] = useState(false);
  const toggleDrawer = () => setOpen(!isOpen);

  return (
    <ThemeProvider darkMode={darkMode}>
      <Header toggleMenu={toggleDrawer} handleChange={toggleDarkMode} />
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
    </ThemeProvider>
  );
}

export default App;
