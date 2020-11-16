import React, { useEffect } from "react";
import { Button } from "@material-ui/core";

import { AuthProvider } from "./utils/authentication";
import { SnackbarProvider } from "notistack";

import { Provider } from "react-redux";
import thunk from "redux-thunk";
import reducer from "./reducers/index";
import { createStore, applyMiddleware } from "redux";
import PageContainer from "./components/pagecontainer/PageContainer";

const middleware = [thunk];
const store = createStore(reducer, applyMiddleware(...middleware));

function App() {
  const notistackRef = React.createRef();
  const onClickDismiss = (key) => () => {
    notistackRef.current.closeSnackbar(key);
  };

  return (
    <Provider store={store}>
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
          <PageContainer />
        </AuthProvider>
      </SnackbarProvider>
    </Provider>
  );
}

export default App;
