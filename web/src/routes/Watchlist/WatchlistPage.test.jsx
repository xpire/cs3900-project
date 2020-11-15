import WatchlistPage from "./WatchlistPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

import { Provider } from "react-redux";
import reducer from "../../reducers/index";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

const middleware = [thunk];
const store = createStore(reducer, applyMiddleware(...middleware));

describe("Watchlist Page", () => {
  it("renders Table correctly", () => {
    const { getByText } = render(
      <Provider store={store}>
        <BrowserRouter>
          <SnackbarProvider>
            <WatchlistPage />
          </SnackbarProvider>
        </BrowserRouter>
      </Provider>
    );
    const TitleElement = getByText("Watch List");
    expect(TitleElement).toBeInTheDocument();
  });
});
