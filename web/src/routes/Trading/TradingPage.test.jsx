import React from "react";
import { render } from "@testing-library/react";
import TradingPage from "./TradingPage";

describe("Trading Page", () => {
  it("Contains important buttons", () => {
    const { getByText } = render(<TradingPage />);
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
