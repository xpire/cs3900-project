import { combineReducers } from "redux";

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

const user = (state = initialState.user, action) => {
  console.log("action type: " + action.type);
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

export const getUser = (state) => state.user;
export default combineReducers({ user, stocks });
