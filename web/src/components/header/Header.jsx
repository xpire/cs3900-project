import React, { useContext, useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Switch,
  useScrollTrigger,
  Slide,
  Grid,
  Link as MaterialLink,
} from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import styled from "styled-components";
import { useHistory, useLocation, Link } from "react-router-dom";

import app from "../../utils/firebase";
import { AuthContext } from "../../utils/authentication";
import { locationToRoutes, Routes } from "../../utils/routes";

const HeaderButton = styled(Button)`
  // color: white;
`;

const HeaderTitle = styled(Typography)`
  flex-grow: 1;
`;

const StyledMenu = styled(MenuIcon)({ color: "white" });

const StyledLink = styled(Button)`
  color: white;
`;
const MyHeader = ({ toggleMenu, handleChange }) => {
  const trigger = useScrollTrigger({ target: window }); // disable Slide for now
  const { user } = useContext(AuthContext);
  let location = useLocation();
  const [headerTitle, setHeaderTitle] = useState("Investment Simulator");

  const getTitle = (loc) => {
    const majorLocation = loc.match(/^\/[^\/]*/)[0];
    if (majorLocation in locationToRoutes) {
      return locationToRoutes[majorLocation];
    } else {
      return "Xecute";
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
          <IconButton edge="start" onClick={toggleMenu}>
            <StyledMenu />
          </IconButton>
          <HeaderTitle variant="h4">{headerTitle}</HeaderTitle>
          {/* <Grid container direction="row" justify="flex-end" spacing={2}>
            {Routes.filter(
              ({ isPublic, isShown }) =>
                isShown && (user ? !isPublic : isPublic)
            ).map(({ text, path }) => (
              <Grid item>
                <StyledLink component={Link} to={path} variant="outlined">
                  {text}
                </StyledLink>
              </Grid>
            ))}
          </Grid> */}
          <Switch onChange={handleChange} color="secondary" />
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