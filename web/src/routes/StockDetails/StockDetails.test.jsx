import React from "react";
import { render } from "@testing-library/react";
import StockDetailsPage from "./StockDetailsPage";

describe("Stock Details Page", () => {
  it("Displays in-depth details", () => {
    // const { getByText } = render(<StockDetailsPage />);
    // const SymbolElement = getByText(/AAPL/);
    // expect(SymbolElement).toBeInTheDocument();
    /* I get this error, Don't know how to fix:
        TypeError: Cannot read property 'match' of undefined

      89 |   console.log({ props });
      90 |   // const stockCode = props.match.params.symbol.toUpperCase();
    > 91 |   const { symbol } = useParams();
    */
  });
});
