import React from "react";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import Switch from "@material-ui/core/Switch";
import useScrollTrigger from "@material-ui/core/useScrollTrigger";
import Slide from "@material-ui/core/Slide";
import { createStyles, makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) =>
  createStyles({
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
  })
);

const MyHeader = ({ toggleMenu, handleChange }) => {
  const classes = useStyles();
  const trigger = useScrollTrigger({ target: window }); // disable Slide for now
  return (
    <Slide appear={false} direction="down" in={!trigger}>
      <AppBar position="sticky">
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            onClick={toggleMenu}
          >
            <MenuIcon />
          </IconButton>
          <Typography className={classes.title} color="textPrimary">
            Menu
          </Typography>
          <Switch onChange={handleChange} color="secondary"></Switch>
          <Button>Login</Button>
        </Toolbar>
      </AppBar>
    </Slide>
  );
};

export default MyHeader;
