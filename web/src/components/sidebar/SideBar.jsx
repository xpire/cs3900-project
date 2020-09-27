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
import HomeIcon from "@material-ui/icons/Home";
import { Link } from "react-router-dom";
import styled from "styled-components";

import { Routes } from "../../App";
import { AuthContext } from "../../utils/authentication";

const StyledSideBar = styled.div`
  padding: 20px;
`;

const SideBar = ({ isOpen, handleChange }) => {
  const { user } = useContext(AuthContext);
  return (
    <Drawer open={isOpen} onClose={handleChange}>
      <StyledSideBar>
        <Grid container justify="space-evenly">
          <Grid item xs={12}>
            <Typography variant="h4">Menu</Typography>
          </Grid>
        </Grid>
      </StyledSideBar>
      <List onClick={handleChange} onKeyDown={handleChange}>
        {Routes.filter(({ isPublic }) => (user ? !isPublic : isPublic)).map(
          ({ text, path }) => (
            <ListItem button key={text} component={Link} to={path}>
              <ListItemIcon>
                <HomeIcon />
              </ListItemIcon>
              <ListItemText>{text}</ListItemText>
            </ListItem>
          )
        )}
      </List>
    </Drawer>
  );
};

export default SideBar;
