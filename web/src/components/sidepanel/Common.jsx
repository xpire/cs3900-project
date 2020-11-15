import React from "react";
import { Grid, Box, Divider, Typography } from "@material-ui/core";

import { format } from "../../utils/formatter";
import ColoredText from "../common/ColoredText";

export const VALUE_SIZE = 14;
export const SUBVALUE_SIZE = 11;

export function ComputeChanges(price, open) {
  const change = price - open;
  const changePercentage = (100 * change) / open;
  return [change, changePercentage];
}

export function NumericColoredText({
  value,
  text,
  fontSize,
  color,
  showTxtColor = true,
  align = "right",
}) {
  return (
    <div style={{ textAlign: align }}>
      <ColoredText
        color={showTxtColor ? (value > 0 ? "green" : "red") : null}
        style={{ fontSize, display: "inline" }}
        delta={color}
        align={align}
      >
        {text}
      </ColoredText>
    </div>
  );
}

function ValueLabel(label) {
  return <Typography style={{ fontSize: VALUE_SIZE }}>{label}</Typography>;
}

function SubvalueLabel(label) {
  return (
    <Typography color="textSecondary" style={{ fontSize: SUBVALUE_SIZE }}>
      {label}
    </Typography>
  );
}

export function PanelListHeader({
  label1,
  label2,
  sublabel1 = null,
  sublabel2 = null,
}) {
  const frags = {
    frag1: ValueLabel(label1),
    frag2: ValueLabel(label2),
    subfrag1: sublabel1 === null ? null : SubvalueLabel(sublabel1),
    subfrag2: sublabel2 === null ? null : SubvalueLabel(sublabel2),
  };
  return (
    <>
      <div style={{ padding: "0px 16px 4px 16px" }}>
        <PanelListItem {...frags} />
      </div>
      <Divider />
      <Divider />
      <Divider />
    </>
  );
}

export function PanelListItem({ frag1, frag2, subfrag1, subfrag2 }) {
  return (
    <Grid container>
      <Grid item xs={5}>
        {frag1}
        {subfrag1 !== null && subfrag1}
      </Grid>
      <Grid item xs={7}>
        <div style={{ textAlign: "right" }}>
          {frag2}
          {subfrag2 !== null && subfrag2}
        </div>
      </Grid>
    </Grid>
  );
}

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
