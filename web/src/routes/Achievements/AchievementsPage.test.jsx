import AchievementsPage from "./AchievementsPage";
import React from "react";
import { render, screen, waitForElement } from "@testing-library/react";
import { AuthContext } from "../../utils/authentication";
import axios from "axios";

import * as mockedData from "../../stubby/user/achievements.json";

// Our mocked response
const axiosResponse = {
  data: mockedData,
  status: 200,
  statusText: "OK",
  config: {},
  headers: {},
};

describe("Achievements Page", () => {
  let mock;

  beforeEach(() => {
    mock = jest.spyOn(axios, "get").mockImplementation(() =>
      Promise.resolve({
        axiosResponse,
      })
    );
  });

  afterEach(() => {
    mock.mockRestore();
  });

  it("Shows user name from AuthContext", () => {
    // const get = jest.fn();
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <AchievementsPage />
      </AuthContext.Provider>
    );
    const linkElement = getByText(/admin@ecksdee.com/i);
    expect(linkElement).toBeInTheDocument();
  });
  it("Shows correct Information", () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
        <AchievementsPage />
      </AuthContext.Provider>
    );
    const UnlockedAchievementsElement = getByText(/Unlocked Achievements/i);
    expect(UnlockedAchievementsElement).toBeInTheDocument();
    const LevelElement = getByText(/Level/i);
    expect(LevelElement).toBeInTheDocument();
  });
  // it("Shows Achievements Card Grid", async () => {
  //   render(
  //     <AuthContext.Provider value={{ user: { email: "admin@ecksdee.com" } }}>
  //       <AchievementsPage />
  //     </AuthContext.Provider>
  //   );
  //   // mockedData.default.map(async ({ name }) => {

  //   //   // console.log({ visibleText });
  //   //   // console.log({ name });
  //   //   // console.log({ name, visibleText });
  //   //   // expect(visibleText).toEqual("sssssss");
  //   //   // expect(visibleText).toHaveLength(1);
  //   // });
  //   // waitFor has an error, cannot use
  //   // await waitFor(() => {
  //   //   // expect(getByText('the lion king')).toBeInTheDocument()
  //   //   expect(screen.getByText("Max Level!")).toBeInTheDocument();
  //   // });

  //   // const e = await waitForElement(() => screen.getByText("Max Level!"));
  //   // expect(e.toBeInTheDocument());
  //   // await waitFor(() => expect(getByText("Good start")).toBeInTheDocument());
  //   // waitFor(
  //   //   mockedData.default.map((s) =>
  //   //     expect(getByText(s.name)).toBeInTheDocument()
  //   //   )
  //   // );
  // });
});
