import React from "react";
import { Grid, Box, Typography } from "@material-ui/core";

import { format } from "../../utils/formatter";

export function HalfGridItem({ label, value, numeric = true }) {
  const formattedValue = numeric ? `$${format(value)}` : value;
  return (
    <Grid item xs={6} key={label}>
      <Typography
        variant="caption"
        color="textSecondary"
        style={{ fontSize: 11 }}
      >
        {label}
      </Typography>
      <Typography style={{ fontSize: 14 }}>{formattedValue}</Typography>
    </Grid>
  );
}

export function Spacing() {
  return <Box p={0.5} />;
}
