import React from "react";
import { render } from "@testing-library/react";
import StockDetailsPage from "./StockDetailsPage";

describe("Stock Details Page", () => {
  jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useParams: () => ({
      push: jest.fn(),
    }),
  }));
  it("Displays in-depth details: symbol", () => {
    const { getByText } = render(<StockDetailsPage />);
    const SymbolElement = getByText(/AAPL/);
    expect(SymbolElement).toBeInTheDocument();
  });
  it("Displays in-depth details: name", () => {
    const { getByText } = render(<StockDetailsPage />);
    const SymbolElement = getByText(/Apple\ Inc/);
    expect(SymbolElement).toBeInTheDocument();
  });
});
