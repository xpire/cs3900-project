import React, { useContext } from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  Typography,
  Grid,
} from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import { Link } from "react-router-dom";
import styled from "styled-components";

import { Routes } from "../../utils/routes";
import { AuthContext } from "../../utils/authentication";
import Logo from "../../ecksdeeLogo.png.svg";

const StyledSideBar = styled.div`
  padding: 20px;
  width: 240px;
`;

const SideBar = ({ isOpen, handleChange, variant }) => {
  const { user } = useContext(AuthContext);
  return (
    <Drawer open={isOpen} onClose={handleChange} variant={variant}>
      <StyledSideBar>
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

export default SideBar;
