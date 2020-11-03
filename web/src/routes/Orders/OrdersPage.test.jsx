import OrdersPage from "./OrdersPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

describe("Orders Page", () => {
  it("renders Table correctly", () => {
    const { getByText } = render(
      <BrowserRouter>
        <SnackbarProvider>
          <OrdersPage />
        </SnackbarProvider>
      </BrowserRouter>
    );
    const TitleElement = getByText("Limit Orders");
    expect(TitleElement).toBeInTheDocument();
  });
});
