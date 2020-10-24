import HomePage from "./HomePage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

describe("Home Page", () => {
  it("renders correctly", () => {
    const { getByText } = render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    const TitleElement = getByText("Execute the Deal");
    expect(TitleElement).toBeInTheDocument();
  });
});
