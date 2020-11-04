import HomePage from "./HomePage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { AuthContext } from "../../utils/authentication";

describe("Home Page", () => {
  it("renders correctly", () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <BrowserRouter>
          <HomePage />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    const TitleElement = getByText("Execute the Deal");
    expect(TitleElement).toBeInTheDocument();
  });
});
