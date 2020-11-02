import ProfilePage from "./ProfilePage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";
import { AuthContext } from "../../utils/authentication";

describe("Profile Page", () => {
  it("renders Table correctly", () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <BrowserRouter>
          <SnackbarProvider>
            <ProfilePage />
          </SnackbarProvider>
        </BrowserRouter>
      </AuthContext.Provider>
    );
    const TitleElement = getByText("Transaction History");
    expect(TitleElement).toBeInTheDocument();
  });
});
