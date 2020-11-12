import { combineReducers } from "redux";
import axios from "../utils/api";

export const UPDATE_USER = "UPDATE_USER";
export const UPDATE_WATCHLIST = "UPDATE_WATCHLIST";
export const UPDATE_STOCKS = "UPDATE_STOCKS";
// export const ADD_TO_WATCHLIST = "ADD_TO_WATCHLIST";
export const REMOVE_FROM_WATCHLIST = "REMOVE_FROM_WATCHLIST";

const initialState = {
  user: {
    basic: {
      username: "",
      email: "",
      level: 1,
      exp: 0.0,
      exp_until_next_level: 0.0,
      exp_threshold: 0.0,
      is_max_level: false,
      last_reset: "",
      resets: 0,
    },
    watchlist: [],
    orders: [],
    transactions: [],
    porfolio: {
      long: [],
      short: [],
    },
    stats: {
      // closing values
      total_long_value: 0.0,
      total_short_value: 0.0,
      total_portfolio_value: 0.0,

      // profit
      total_long_profit: 0.0,
      total_short_profit: 0.0,
      total_portfolio_profit: 0.0,

      // return
      total_long_return: 0.0,
      total_short_return: 0.0,
      total_portfolio_return: 0.0,

      // daily profit
      daily_long_profit: 0.0,
      daily_short_profit: 0.0,
      daily_portfolio_profit: 0.0,

      // daily return
      daily_long_return: 0.0,
      daily_short_return: 0.0,
      daily_portfolio_return: 0.0,

      // other
      balance: 0.0,
      short_balance: 0.0,
      total_value: 0.0,
    },
    leaderboard: {
      rankings: [],
      user_ranking: 1,
    },
  },
  stocks: [],
};

/*
  REDUCERS
*/
const user = (state = initialState.user, action) => {
  switch (action.type) {
    case UPDATE_USER:
      return action.user;
    case UPDATE_WATCHLIST:
      return { ...state, watchlist: action.watchlist };
    case REMOVE_FROM_WATCHLIST:
      const watchlist = state.watchlist.filter(
        (stock) => stock.symbol !== action.symbol
      );
      return { ...state, watchlist };
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

/*
  action creators
*/
// https://redux.js.org/recipes/reducing-boilerplate#action-creators
function makeActionCreator(type, ...argNames) {
  return function(...args) {
    const action = { type };
    argNames.forEach((arg, index) => {
      action[argNames[index]] = args[index];
    });
    return action;
  };
}

const updateUser = makeActionCreator(UPDATE_USER, "user");
const updateWatchlist = makeActionCreator(UPDATE_WATCHLIST, "watchlist");
const removeFromWatchlistSync = makeActionCreator(
  REMOVE_FROM_WATCHLIST,
  "symbol"
);

/*
  ACTIONS
*/
function reloadFromAPI(endpoint, updateFn) {
  return () =>
    function(dispatch) {
      axios.get(endpoint).then(
        (response) => dispatch(updateFn(response.data)),
        (error) => console.log("ERROR reloading from " + endpoint)
      );
    };
}

export const reloadUser = reloadFromAPI("/user/detail", updateUser);
// export const reloadWatchlist = reloadFromAPI("/watchlist", updateWatchlist);

export function addToWatchlist(symbol) {
  return function(dispatch) {
    axios.post(`/watchlist?symbol=${symbol}`).then(
      (response) => dispatch(updateWatchlist(response.data)),
      (error) => console.log("ERROR")
    );
  };
}

export function removeFromWatchlist(symbol) {
  return function(dispatch) {
    dispatch(removeFromWatchlistSync(symbol)); // make the change visible quickly
    axios.delete(`/watchlist?symbol=${symbol}`).then(
      (response) => dispatch(updateWatchlist(response.data)),
      (error) => console.log("ERROR")
    );
  };
}
