import React, { useContext, useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  useScrollTrigger,
  Slide,
  Box,
} from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import styled from "styled-components";
import { useHistory, useLocation } from "react-router-dom";

import axios from "../../utils/api";
import app from "../../utils/firebase";
import { AuthContext } from "../../utils/authentication";
import { locationToRoutes } from "../../utils/routes";
import Logo from "../../logo.svg";

const HeaderButton = styled(Button)`
  // color: white;
`;

const HeaderTitle = styled(Typography)`
  flex-grow: 1;
`;

const ElevationScroll = ({ children }) => {
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 0,
  });

  return React.cloneElement(children, {
    elevation: trigger ? 4 : 0,
  });
};

/**
 * Header component for the website, with a button which opens the SideBar component
 */
const MyHeader = ({ toggleMenu }) => {
  const { user } = useContext(AuthContext);
  let location = useLocation();
  const [headerTitle, setHeaderTitle] = useState("Investment Simulator");

  const getTitle = (loc) => {
    const majorLocation = loc.match(/^\/[^/]*/)[0];
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
    delete axios.defaults.headers.common["id-token"];
    console.log("header now:", axios.defaults.headers.common["id-token"]);
    history.push("/");
  };

  const handleLogin = () => {
    history.push("/signin");
  };

  return (
    <Box zIndex={1201}>
      <ElevationScroll>
        <AppBar position="fixed" color="secondary">
          <Toolbar>
            <IconButton edge="start" onClick={toggleMenu}>
              <img src={Logo} alt="X" height="40px" />
            </IconButton>
            <HeaderTitle variant="h4">{headerTitle}</HeaderTitle>
            {user ? (
              <HeaderButton
                variant="contained"
                color="primary"
                onClick={handleLogout}
              >
                Sign Out
              </HeaderButton>
            ) : (
              <HeaderButton
                variant="contained"
                color="primary"
                onClick={handleLogin}
              >
                Sign In
              </HeaderButton>
            )}
          </Toolbar>
        </AppBar>
      </ElevationScroll>
    </Box>
  );
};

export default MyHeader;
// export default styled(MyHeader)`
//   height: 10vh;
// `;
