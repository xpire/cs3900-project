import SupportPage from "./SupportPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";
import { AuthContext } from "../../utils/authentication";

describe("Support Page", () => {
  it("renders Tutorials correctly", () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <BrowserRouter>
          <SnackbarProvider>
            <SupportPage />
          </SnackbarProvider>
        </BrowserRouter>
      </AuthContext.Provider>
    );
    const TitleElement = getByText("Tutorials");
    expect(TitleElement).toBeInTheDocument();
  });
});
