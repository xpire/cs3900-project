import React from "react";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import { ThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
// import purple from "@material-ui/core/colors/purple";
// import grey from "@material-ui/core/colors/grey";

const MyThemeProvider = ({ children, darkMode }) => {
  const prefersDarkMode =
    useMediaQuery("(prefers-color-scheme: dark)") || darkMode;
  const elements = [
    "MuiAppBar",
    "MuiBackdrop",
    "MuiButton",
    "MuiCard",
    "MuiCheckbox",
    "MuiChip",
    "MuiDialog",
    "MuiDivider",
    "MuiDrawer",
    "MuiAccordion",
    "MuiExpansionPanel",
    "MuiLink",
    "MuiMenu",
    "MuiMenuItem",
    "MuiPaper",
    "MuiTab",
  ];

  const commonTheme = {
    overrides: Object.fromEntries(
      elements.map((elem) => {
        return [
          [elem],
          {
            root: {
              transition: "background 0.25s linear",
            },
          },
        ];
      })
    ),
  };

  const darkTheme = createMuiTheme({
    ...commonTheme,
    palette: {
      // primary: {
      //   main: grey[700],
      // },
      // secondary: {
      //   main: purple[500],
      // },
      type: "dark",
    },
  });

  const lightTheme = createMuiTheme({
    palette: {
      // primary: {
      //   main: "#CAA8F5",
      //   light: "#9A50B9",
      //   dark: "#462255",
      // },
      // secondary: {
      //   main: lightGreen[500],
      // },
    },
  });
  // structure: https://material-ui.com/customization/default-theme/#default-theme

  return (
    <ThemeProvider theme={!prefersDarkMode ? lightTheme : darkTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
};

export default MyThemeProvider;
