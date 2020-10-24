import LoginComponent from "./LoginComponent";
import React from "react";
import { render, fireEvent } from "@testing-library/react";

describe("LoginComponent", () => {
  it("Runs submitHandler on button press", () => {
    const handleClick = jest.fn();
    const { getByRole } = render(
      <LoginComponent
        buttonText="thisIsATestElement"
        submitHandler={handleClick}
      />
    );
    const buttonElement = getByRole("button");
    fireEvent.click(buttonElement);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("Disables button when loading", () => {
    const handleClick = jest.fn();
    const { getByText, getByRole } = render(
      <LoginComponent
        buttonText="thisIsATestElement"
        submitHandler={handleClick}
        loading={true}
      />
    );
    const buttonElement = getByRole("button");
    fireEvent.click(buttonElement);
    expect(handleClick).toHaveBeenCalledTimes(0);
  });
});
