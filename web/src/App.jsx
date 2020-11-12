import React from "react";
import { useHistory } from "react-router-dom";
import {
  Button,
  Card,
  Toolbar,
  Typography,
  AppBar,
  CssBaseline,
} from "@material-ui/core";
// import Hidden from "@material-ui/core/Hidden";

import { AuthProvider } from "./utils/authentication";
import { SnackbarProvider } from "notistack";
import ScrollToTop from "./utils/scrollToTop";

import { Provider } from "react-redux";
import thunk from "redux-thunk";
import reducer from "./reducers/index";
import { createStore, applyMiddleware } from "redux";
import PageContainer from "./components/pagecontainer/PageContainer";

const middleware = [thunk];
const store = createStore(reducer, applyMiddleware(...middleware));

function App() {
  const history = useHistory();

  const notistackRef = React.createRef();
  const onClickDismiss = (key) => () => {
    notistackRef.current.closeSnackbar(key);
  };
  return (
    <SnackbarProvider
      anchorOrigin={{
        vertical: "top",
        horizontal: "center",
      }}
      preventDuplicate
      ref={notistackRef}
      action={(key) => <Button onClick={onClickDismiss(key)}>OK</Button>}
    >
      <AuthProvider>
        <ScrollToTop history={history}>
          <Provider store={store}>
            <PageContainer />
          </Provider>
        </ScrollToTop>
      </AuthProvider>
    </SnackbarProvider>
  );
}

export default App;
