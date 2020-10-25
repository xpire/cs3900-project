import React from "react";
import Alert from "./Alert";
import {
  render,
  screen,
  waitForElement,
  fireEvent,
} from "@testing-library/react";

describe("Alert Component", () => {
  it("Shows correct information", () => {
    const { getByText } = render(
      <Alert
        title="testTitle"
        text="testText"
        open={true}
        handleClose={() => {}}
        isError={false}
      />
    );
    const titleElement = getByText("testTitle");
    expect(titleElement).toBeInTheDocument();
    const textElement = getByText("testText");
    expect(textElement).toBeInTheDocument();
  });
  it("calls handleClose on close", () => {
    const handleClose = jest.fn();
    const { getByText } = render(
      <Alert
        title="testTitle"
        text="testText"
        open={true}
        handleClose={handleClose}
        isError={false}
      />
    );
    const closeElement = getByText("OK");
    fireEvent.click(closeElement);
    expect(handleClose).toHaveBeenCalledTimes(1);
  });
});
