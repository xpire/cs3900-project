import React from "react";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import HomeIcon from "@material-ui/icons/Home";
import MaterialLink from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { Link } from "react-router-dom";

const items = [
  { text: "Home", path: "/" },
  { text: "Sign In", path: "/login" },
];

const SideBar = ({ isOpen, handleChange }) => {
  return (
    <Drawer open={isOpen} onClose={handleChange}>
      <Grid container justify="space-evenly">
        <Grid item xs={12}>
          <Typography variant="h4">Welcome!</Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5">Website</Typography>
        </Grid>
      </Grid>
      <List onClick={handleChange} onKeyDown={handleChange}>
        {items.map(({ text, path }) => (
          <ListItem button key={text} component={Link} to={path}>
            <ListItemIcon>
              <HomeIcon />
            </ListItemIcon>
            <ListItemText>
              <MaterialLink color="textPrimary" underline="none">
                {text}
              </MaterialLink>
            </ListItemText>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default SideBar;
