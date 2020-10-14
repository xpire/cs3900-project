import React from "react";
// import useMediaQuery from "@material-ui/core/useMediaQuery";
import { ThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";

const MyThemeProvider = ({ children }) => {
  const prefersDarkMode = true;
  // useMediaQuery("(prefers-color-scheme: dark)") || darkMode;
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
      secondary: {
        main: "#424242",
      },
      primary: {
        main: "#2196f3",
      },
      type: "dark",
    },
  });

  const lightTheme = createMuiTheme({
    ...commonTheme,
    palette: {
      secondary: {
        main: "#2196f3",
      },
      primary: {
        main: "#1769aa",
      },
      type: "light",
    },
  });
  // structure: https://material-ui.com/customization/default-theme/#default-theme

  return (
    <ThemeProvider theme={prefersDarkMode ? darkTheme : lightTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
};

export default MyThemeProvider;
