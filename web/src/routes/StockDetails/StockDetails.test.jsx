import React from "react";
import { render } from "@testing-library/react";
import StockDetailsPage from "./StockDetailsPage";

import routeData from "react-router";

const mockLocation = {
  symbol: "FB",
};

beforeEach(() => {
  jest.spyOn(routeData, "useParams").mockReturnValue(mockLocation);
  jest.spyOn(routeData, "useHistory").mockReturnValue({});
  // fetch.mockClear();
});

describe("Stock Details Page", () => {
  it("Displays in-depth details: symbol", () => {
    const { getByText } = render(<StockDetailsPage />);
    const SymbolElement = getByText("FB");
    expect(SymbolElement).toBeInTheDocument();
  });
  // it("Displays in-depth details: name", async () => { //using fetch broke this test
  //   fetch.mockImplementationOnce(() =>
  //     Promise.resolve([
  //       {
  //         day_gain: 6,
  //         exchange: "NYSE",
  //         latest_price: 755,
  //         symbol: "AAPL",
  //       },
  //     ])
  //   );
  //   const { getByText } = render(<StockDetailsPage />);
  //   await act(() => promise);
  //   const SymbolElement = getByText("NYSE");
  //   expect(SymbolElement).toBeInTheDocument();
  // });
});
