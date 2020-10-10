import React from "react";
import { TextField, Grid, Button } from "@material-ui/core";

const Login = ({ buttonText, submitHandler, repeat }) => {
  return (
    <form noValidate onSubmit={submitHandler}>
      <Grid container spacing={2}>
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
        <Grid item xs={12}>
          <TextField
            variant="outlined"
            required
            fullWidth
            id="password"
            name="password"
            label="password"
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
              label="repeat password"
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
