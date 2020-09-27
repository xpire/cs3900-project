import React, { useContext } from "react";
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
import { useHistory } from "react-router-dom";

import app from "../../utils/firebase";
import { AuthContext } from "../../utils/authentication";

const HeaderButton = styled(Button)`
  color: white;
`;

const HeaderTitle = styled(Typography)`
  flex-grow: 1;
`;

const HeaderIcon = styled(IconButton)`
  margin-right: 20px;
  color: white;
`;

const MyHeader = ({ toggleMenu, handleChange }) => {
  const trigger = useScrollTrigger({ target: window }); // disable Slide for now
  const { user } = useContext(AuthContext);
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
          <HeaderTitle>Investment Simulator</HeaderTitle>
          <Switch onChange={handleChange} color="secondary"></Switch>
          {user ? (
            <HeaderButton onClick={handleLogout}>logout</HeaderButton>
          ) : (
            <HeaderButton onClick={handleLogin}>login</HeaderButton>
          )}
        </Toolbar>
      </AppBar>
    </Slide>
  );
};

export default MyHeader;
