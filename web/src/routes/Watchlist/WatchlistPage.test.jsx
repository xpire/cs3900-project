import WatchlistPage from "./WatchlistPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

describe("Watchlist Page", () => {
  it("renders Table correctly", () => {
    const { getByText } = render(
      <BrowserRouter>
        <SnackbarProvider>
          <WatchlistPage />
        </SnackbarProvider>
      </BrowserRouter>
    );
    const TitleElement = getByText("Watch List");
    expect(TitleElement).toBeInTheDocument();
  });
});
