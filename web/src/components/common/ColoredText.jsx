import React, { useState, useEffect } from "react";
import {
  Typography,
  styled as materialStyled,
  useTheme,
} from "@material-ui/core";
import { useDelta } from "react-delta";

const StyledColoredText = materialStyled(Typography)({
  color: (props) => props.color,
  display: "inline",
});

export const green = {
  dark: "#c1ff7a",
  light: "#689f38",
  background: "rgba(193,255,122,0.5)",
};
export const red = {
  dark: "#ef5350",
  light: "#f50057",
  background: "rgba(239,83,80,0.5)",
};
/**
 * A React hook which works in tandem with ColorText to animate a green/red highlight when the text has changed.
 */
export const useColoredText = (value) => {
  const myDelta = useDelta(value);
  const [delta, setDelta] = useState(0);
  const fadeInAndOut = (flag) => {
    setDelta(flag);
    setTimeout(() => setDelta(0), 1000);
  };
  useEffect(() => {
    console.log("delta effect");
    if (myDelta && myDelta.prev && myDelta.prev !== "NaN") {
      console.log(myDelta);
      const prev =
        typeof myDelta.prev === "string"
          ? parseFloat(myDelta.prev.replace(/[%$+]*/g, ""))
          : myDelta.prev;
      const curr =
        typeof myDelta.curr === "string"
          ? parseFloat(myDelta.curr.replace(/[%$+]*/g, ""))
          : myDelta.curr;
      console.log({ prev, curr });
      if (prev < curr) {
        console.log("highlight Green");
        fadeInAndOut(1);
      } else {
        console.log("highlight Red");
        fadeInAndOut(-1);
      }
    }
  }, [myDelta]);
  return [delta];
};

/**
 * A Component which shows colored text built on the material-ui Typography component.
 */
const ColoredText = ({ children, color, delta, style, ...restProps }) => {
  const theme = useTheme();
  return (
    <StyledColoredText
      style={{
        ...style,
        color:
          color === "green"
            ? green[theme.palette.type]
            : color === "red"
            ? red[theme.palette.type]
            : "#fff",
        background:
          delta > 0
            ? green["background"]
            : delta < 0
            ? red["background"]
            : "none",
        transition: "background 1s ease-out",
      }}
      {...restProps}
    >
      {children}
    </StyledColoredText>
  );
};

export default ColoredText;
