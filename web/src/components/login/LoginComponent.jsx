import React from "react";
import PropTypes from "prop-types";
import { TextField, Grid, Button, LinearProgress } from "@material-ui/core";

/**
 * Login form component used in most authentication pages.
 */
const Login = ({
  buttonText,
  submitHandler,
  repeat = false,
  email = true,
  username = false,
  loading = false,
}) => {
  return (
    <form noValidate onSubmit={submitHandler}>
      <Grid container spacing={2}>
        {username && (
          <Grid item xs={12}>
            <TextField
              name="username"
              variant="outlined"
              required
              fullWidth
              id="username"
              label="Username"
              type="text"
              autoFocus
            />
          </Grid>
        )}
        {email && (
          <Grid item xs={12}>
            <TextField
              name="email"
              variant="outlined"
              required
              fullWidth
              id="email"
              label="Email Address"
              type="email"
              autoFocus
            />
          </Grid>
        )}
        <Grid item xs={12}>
          <TextField
            variant="outlined"
            required
            fullWidth
            id="password"
            name="password"
            label="Password"
            type="password"
          />
        </Grid>
        {repeat && (
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="repeatPassword"
              name="repeatPassword"
              label="Reenter Password"
              type="password"
            />
          </Grid>
        )}
        <Grid item xs={12}>
          {loading && <LinearProgress />}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {buttonText}
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

Login.propTypes = {
  /** Text to display in the button */
  buttonText: PropTypes.string,
  /** submitHandler function that is called on submission */
  submitHandler: PropTypes.func,
  /** Whether to show a second password field for sign up page password verification */
  repeat: PropTypes.bool,
  /** Whether to show an Email field for Login and Sign Up */
  email: PropTypes.bool,
  /** Whether to show a Username field for Sign Up */
  username: PropTypes.bool,
  /** Whether component should display a loading indicator when submission is loading */
  loading: PropTypes.bool,
};

Login.defaultProps = {
  repeat: false,
  email: true,
  username: false,
  loading: false,
};

export default Login;
