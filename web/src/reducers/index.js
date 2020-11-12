import { combineReducers } from "redux";
import axios from "../utils/api";

export const UPDATE_USER = "UPDATE_USER";
const UPDATE_STOCKS = "UPDATE_STOCKS";
// const WATCHLIST = "WATCHLIST";
// const RANKINGS = "RANKINGS";

const initialState = {
  user: {
    username: "Ian Park",
    rank: 3,
    level: 10,
    exp: 100,
    exp_until_next_level: 400,
    net_worth: 100,
    balance: 1000000.12,
    long_value: 20,
    short_balance: 30,
    short_value: 40,
  },
  rankings: [],
  watchlist: [],
  positions: [],
  stocks: [],
};

/*
  REDUCERS
*/
const user = (state = initialState.user, action) => {
  switch (action.type) {
    case UPDATE_USER:
      return action.user;
    default:
      return state;
  }
};

const stocks = (state = initialState.stocks, action) => {
  switch (action.type) {
    case UPDATE_STOCKS:
      return action.stocks;
    default:
      return state;
  }
};

export default combineReducers({ user, stocks });

/*
  SELECTORS
*/
export const getUser = (state) => state.user;

const updateUser = (user) => ({
  type: UPDATE_USER,
  user,
});

/*
  ACTIONS
*/
export function reloadUser() {
  return function(dispatch, getState) {
    console.log("RELOAD USER");
    axios.get("/user/detail").then(
      (response) => dispatch(updateUser(response.data)),
      (error) => console.log("ERROR")
    );
  };
}
