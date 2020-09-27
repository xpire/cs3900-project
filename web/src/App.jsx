import React, { useState } from "react";
import { Switch, useLocation } from "react-router-dom";

import ThemeProvider from "./utils/ThemeProvider";
import Header from "./components/header/Header";
import Drawer from "./components/sidebar/SideBar";
import HomePage from "./routes/HomePage";
import LoginPage from "./routes/LoginPage";
import SignUpPage from "./routes/SignUpPage";
import DashboardPage from "./routes/DashboardPage";
import ForgotPasswordPage from "./routes/ForgotPasswordPage";
import PrivateRoute from "./utils/PrivateRoute";

export const Routes = [
  { text: "Home", path: "/", component: HomePage, isPublic: true, exact: true },
  {
    text: "Sign In",
    path: "/signin",
    component: LoginPage,
    isPublic: true,
    exact: false,
  },
  {
    text: "Sign Up",
    path: "/signup",
    component: SignUpPage,
    isPublic: true,
    exact: false,
  },
  {
    text: "Forgot Password",
    path: "/forgot",
    component: ForgotPasswordPage,
    isPublic: true,
    exact: false,
  },
  {
    text: "Dashboard",
    path: "/home",
    component: DashboardPage,
    isPublic: false,
    exact: false,
  },
];

function App() {
  const location = useLocation();

  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => setDarkMode(!darkMode);

  const [isOpen, setOpen] = useState(false);
  const toggleDrawer = () => setOpen(!isOpen);

  return (
    <ThemeProvider darkMode={darkMode}>
      <Header toggleMenu={toggleDrawer} handleChange={toggleDarkMode} />
      <Drawer isOpen={isOpen} handleChange={toggleDrawer} />
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
