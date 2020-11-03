import PortfolioPage from "./PortfolioPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

describe("Portfolio Page", () => {
  it("renders Table correctly", () => {
    const { getByText } = render(
      <BrowserRouter>
        <SnackbarProvider>
          <PortfolioPage />
        </SnackbarProvider>
      </BrowserRouter>
    );
    const TitleElement = getByText("Portfolio");
    expect(TitleElement).toBeInTheDocument();
  });
});
