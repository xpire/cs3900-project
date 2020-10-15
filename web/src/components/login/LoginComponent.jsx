import React from "react";
import { TextField, Grid, Button } from "@material-ui/core";

const Login = ({
  buttonText,
  submitHandler,
  repeat = false,
  email = true,
  username = false,
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
          <Button type="submit" fullWidth variant="contained" color="primary">
            {buttonText}
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default Login;
