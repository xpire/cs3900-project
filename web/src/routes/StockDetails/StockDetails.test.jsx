import React from "react";
import { render } from "@testing-library/react";
import StockDetailsPage from "./StockDetailsPage";

import routeData from "react-router";

const mockLocation = {
  symbol: "AAPL",
};
beforeEach(() => {
  jest.spyOn(routeData, "useParams").mockReturnValue(mockLocation);
});

describe("Stock Details Page", () => {
  it("Displays in-depth details: symbol", () => {
    const { getByText } = render(<StockDetailsPage />);
    const SymbolElement = getByText("AAPL");
    expect(SymbolElement).toBeInTheDocument();
  });
  it("Displays in-depth details: name", () => {
    const { getByText } = render(<StockDetailsPage />);
    const SymbolElement = getByText(/Apple\ Inc/);
    expect(SymbolElement).toBeInTheDocument();
  });
});
