import { combineReducers } from "redux";
import axios from "../utils/api";

export const UPDATE_USER = "UPDATE_USER";
export const UPDATE_WATCHLIST = "UPDATE_WATCHLIST";
export const UPDATE_STOCKS = "UPDATE_STOCKS";

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
      return { ...state, user: { ...state.user, watchlist: action.watchlist } };
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
// export const getUser = (state) => state.user;

const updateUser = (user) => ({
  type: UPDATE_USER,
  user,
});

const updateWatchlist = (watchlist) => ({
  type: UPDATE_WATCHLIST,
  watchlist,
});

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
export const reloadWatchlist = reloadFromAPI("/watchlist", updateWatchlist);

export function addWatchlist(symbol) {
  return function(dispatch) {
    // can sync update functions too
    axios.post(`/watchlist?symbol=${symbol}`).then(
      (response) => dispatch(updateWatchlist(response.data)),
      (error) => console.log("ERROR")
    );
  };
}
