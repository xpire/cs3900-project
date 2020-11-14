import React, { useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
} from "@material-ui/core";
import styled from "styled-components";
import { useLocation } from "react-router-dom";
import { locationToRoutes } from "../../utils/routes";
import Logo from "../../logo.svg";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import { withStyles } from "@material-ui/core/styles";

const HeaderButton = styled(Button)`
  // color: white;
`;

const HeaderTitle = styled(Typography)`
  flex-grow: 1;
`;

const StyledToggleButtonGroup = withStyles((theme) => ({
  root: {
    marginRight: "-18px",
  },
  grouped: {
    margin: theme.spacing(0.75),
    border: "none",
    "&:not(:first-child)": {
      borderRadius: 100,
    },
    "&:first-child": {
      borderRadius: 100,
    },
  },
}))(ToggleButtonGroup);

/**
 * Header component for the website, with a button which opens the SideBar component
 */
const MyHeader = ({
  toggleMenu,
  panels,
  sidePanelState: [sidePanel, setSidePanel],
}) => {
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
  // const { user } = useContext(AuthContext);
  // let history = useHistory();

  // const handleLogout = () => {
  //   app.auth().signOut();
  //   delete axios.defaults.headers.common["id-token"];
  //   console.log("header now:", axios.defaults.headers.common["id-token"]);
  //   history.push("/");
  // };

  // const handleLogin = () => {
  //   history.push("/signin");
  // };

  return (
    <Box zIndex={1201}>
      <AppBar position="fixed" style={{ backgroundColor: "#424242" }}>
        <Toolbar>
          <IconButton edge="start" onClick={toggleMenu}>
            <img src={Logo} alt="X" height="40px" />
          </IconButton>
          <HeaderTitle variant="h4">{headerTitle}</HeaderTitle>

          {/* ICONS */}
          <StyledToggleButtonGroup
            value={sidePanel}
            exclusive
            onChange={(event, selected) => setSidePanel(selected)}
          >
            {panels.map(({ name, icon }) => (
              <ToggleButton value={name}>{icon}</ToggleButton>
            ))}
          </StyledToggleButtonGroup>

          {/* LOGOUT */}
          {/* {user ? (
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
          )} */}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default MyHeader;
