import React, { useContext, useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Switch,
  useScrollTrigger,
  Slide,
} from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import styled from "styled-components";
import { useHistory, useLocation } from "react-router-dom";

import app from "../../utils/firebase";
import { AuthContext } from "../../utils/authentication";
import { locationToRoutes } from "../../utils/routes";

const HeaderButton = styled(Button)`
  // color: white;
`;

const HeaderTitle = styled(Typography)`
  flex-grow: 1;
`;

const HeaderIcon = styled(IconButton)`
  // margin-right: 20px;
  color: white;
`;

const MyHeader = ({ toggleMenu, handleChange }) => {
  const trigger = useScrollTrigger({ target: window }); // disable Slide for now
  const { user } = useContext(AuthContext);
  let location = useLocation();
  const [headerTitle, setHeaderTitle] = useState("Investment Simulator");

  const getTitle = (loc) => {
    if (loc in locationToRoutes) {
      return locationToRoutes[loc];
    } else {
      return "Home";
    }
  };

  useEffect(() => setHeaderTitle(getTitle(location.pathname)), [location]);
  let history = useHistory();

  const handleLogout = () => {
    app.auth().signOut();
    history.push("/");
  };

  const handleLogin = () => {
    history.push("/signin");
  };

  return (
    <Slide appear={false} direction="down" in={!trigger}>
      <AppBar position="sticky">
        <Toolbar>
          <HeaderIcon edge="start" onClick={toggleMenu}>
            <MenuIcon />
          </HeaderIcon>
          <HeaderTitle variant="h4">{headerTitle}</HeaderTitle>
          <Switch onChange={handleChange} color="secondary"></Switch>
          {user ? (
            <HeaderButton
              variant="contained"
              color="secondary"
              onClick={handleLogout}
            >
              logout
            </HeaderButton>
          ) : (
            <HeaderButton
              variant="contained"
              color="secondary"
              onClick={handleLogin}
            >
              login
            </HeaderButton>
          )}
        </Toolbar>
      </AppBar>
    </Slide>
  );
};

export default MyHeader;
