import LeaderboardPage from "./LeaderboardPage";
import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { AuthContext } from "../../utils/authentication";

import routeData from "react-router";

const mockLocation = {
  symbol: "FB",
};

beforeEach(() => {
  jest.spyOn(routeData, "useParams").mockReturnValue(mockLocation);
  jest.spyOn(routeData, "useHistory").mockReturnValue({});
});

describe("Leaderboard Page", () => {
  it("renders correctly", () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <BrowserRouter>
          <LeaderboardPage />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    const TitleElement = getByText(
      "Welcome admin@ecksdee.com to the Leaderboard page!"
    );
    expect(TitleElement).toBeInTheDocument();
  });
});
