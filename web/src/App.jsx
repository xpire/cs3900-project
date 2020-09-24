import React, { useState } from "react";
import { Switch, Route, useLocation } from "react-router-dom";

import ThemeProvider from "./utils/ThemeProvider";
import Header from "./components/Header/Header";
import Drawer from "./components/SideBar/SideBar";
import HomePage from "./routes/Home";
import LoginPage from "./routes/Login";

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
        <Route path="/login">
          <LoginPage />
        </Route>
        <Route path="/">
          <HomePage />
        </Route>
      </Switch>
    </ThemeProvider>
  );
}

export default App;
