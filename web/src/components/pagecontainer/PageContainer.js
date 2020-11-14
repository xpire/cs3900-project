import React, { useEffect, useState } from "react";
import { Switch, useLocation, Route } from "react-router-dom";
import { Toolbar, CssBaseline } from "@material-ui/core";
// import Hidden from "@material-ui/core/Hidden";

import Header from "../header/Header";
import SideBar from "../sidebar/SideBar";
import PrivateRoute from "../../utils/PrivateRoute";
import { Routes } from "../../utils/routes";
import AuthPage from "../../routes/Auth/AuthPage";
import { makeStyles } from "@material-ui/core/styles";
import Hidden from "@material-ui/core/Hidden";
import SidePanel from "../sidepanel/SidePanel";
import { useDispatch } from "react-redux";
import { reloadUser, reloadStocks } from "../../reducers";
import { PANELS, DEFAULT_PANEL_NAME } from "../sidepanel/Panels";

const drawerWidth = 260;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
    border: 0,
    // background: "rgba(0, 0, 0, 0)",
  },
  drawerContainer: {
    overflow: "auto",
  },
  content: {
    flex: 1,
  },
}));

const DATA_UPDATE_INTERVAL = 10000;

export default function PageContainer() {
  const classes = useStyles();
  const location = useLocation();

  // for navigation drawer
  const [isOpen, setOpen] = useState(false);
  const toggleDrawer = () => setOpen(!isOpen);

  // for redux data management
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(reloadUser());
    dispatch(reloadStocks());
    const interval = setInterval(() => {
      dispatch(reloadUser());
      dispatch(reloadStocks()); // TODO optimize so that it only gets triggered on the market page
    }, DATA_UPDATE_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  // for sidepanel control
  const [sidePanel, setSidePanel] = useState(DEFAULT_PANEL_NAME);
  const selectSidePanel = (newPanel) => {
    if (newPanel !== null) {
      setSidePanel(newPanel);
    }
  };
  const panel = PANELS.find((p) => p.name === sidePanel).panel;

  return (
    <div className={classes.root}>
      <CssBaseline />
      {/* Header */}
      <Header
        toggleMenu={toggleDrawer}
        panels={PANELS}
        sidePanelState={[sidePanel, selectSidePanel]}
      />

      {/* Navigation SideBar */}
      <SideBar
        className={classes.drawer}
        isOpen={isOpen}
        handleChange={toggleDrawer}
        variant="temporary"
        zIndex={1202}
      />

      {/* Main panel in the centre */}
      <main className={classes.content}>
        <Toolbar />
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
      </main>

      {/* Side panel on the right */}
      <Hidden smDown>
        <SidePanel classes={classes} panel={panel} />
      </Hidden>
    </div>
  );
}