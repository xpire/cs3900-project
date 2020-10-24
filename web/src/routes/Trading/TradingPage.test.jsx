import React from "react";
import { render } from "@testing-library/react";
import TradingPage from "./TradingPage";
import routeData from "react-router";
import { SnackbarProvider } from "notistack";

const mockLocation = {
  symbol: "FB",
};

beforeEach(() => {
  jest.spyOn(routeData, "useLocation").mockReturnValue(mockLocation);
  jest.spyOn(routeData, "useHistory").mockReturnValue({});
});
describe("Trading Page", () => {
  it("Contains important buttons", () => {
    const { getByText } = render(
      <SnackbarProvider>
        <TradingPage />
      </SnackbarProvider>
    );
    [
      /Buy/i,
      /Sell/i,
      /Short/i,
      /Cover/i,
      /Quantity/i,
      /Value/i,
      /Limit/i,
      /Market/i,
    ].map((e) => {
      const element = getByText(e);
      expect(element).toBeInTheDocument();
    });
  });
});
