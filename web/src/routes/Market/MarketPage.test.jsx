import MarketPage from "./MarketPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

describe("Market Page", () => {
  it("renders search bar correctly", () => {
    const { getByPlaceholderText } = render(
      <BrowserRouter>
        <SnackbarProvider>
          <MarketPage />
        </SnackbarProvider>
      </BrowserRouter>
    );
    const InputElement = getByPlaceholderText("Search");
    expect(InputElement).toBeInTheDocument();
  });
});
