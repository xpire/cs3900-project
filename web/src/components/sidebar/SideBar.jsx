import React, { useContext } from "react";
import PropTypes from "prop-types";
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  Typography,
  Grid,
  CardActionArea,
  Card,
  CardContent,
} from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import { Link } from "react-router-dom";
import styled from "styled-components";

import { Routes } from "../../utils/routes";
import { AuthContext } from "../../utils/authentication";
import Logo from "../../logo.svg";

const StyledSideBar = styled.div`
  padding: 20px;
  width: 240px;
`;
/**
 * SideBar material-ui component used for page navigation
 */
const SideBar = ({ isOpen, handleChange, variant }) => {
  const { user } = useContext(AuthContext);
  return (
    <Drawer open={isOpen} onClose={handleChange} variant={variant}>
      <StyledSideBar>
        <Card elevation={0}>
          <CardActionArea>
            <CardContent onClick={handleChange}>
              <Grid container justify="space-evenly">
                <Grid item xs={12} container direction="row">
                  <Grid item>
                    <img src={Logo} alt="Execute the Deal Logo" height="48px" />
                  </Grid>
                  <Grid item>
                    <Typography variant="h3">ecute</Typography>
                  </Grid>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2">the Deal</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </CardActionArea>
        </Card>
      </StyledSideBar>
      <List onClick={handleChange} onKeyDown={handleChange}>
        {Routes.filter(
          ({ isPublic, isShown }) => isShown && (user ? !isPublic : isPublic)
        ).map(({ text, path, icon }) => (
          <ListItem button key={text} component={Link} to={path}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText>{text}</ListItemText>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

SideBar.propTypes = {
  /** Whether SideBar is currently open */
  isOpen: PropTypes.bool,
  /** a function that is called to close the SideBar */
  handleChange: PropTypes.func,
  /** a string defined by material-ui's SideBar component for specifying whether the drawer is temporary of permanent */
  variant: PropTypes.string,
};

export default SideBar;
