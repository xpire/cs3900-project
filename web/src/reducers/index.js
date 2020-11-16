import { combineReducers } from "redux";
import axios from "../utils/api";
import { createSelector } from "reselect";
import { auth } from "../utils/authentication";

export const UPDATE = "UPDATE";
export const UPDATE_USER = "UPDATE_USER";
export const UPDATE_STOCKS = "UPDATE_STOCKS";
export const UPDATE_WATCHLIST = "UPDATE_WATCHLIST";
export const UPDATE_ORDERS = "UPDATE_ORDERS";
export const ADD_TO_WATCHLIST = "ADD_TO_WATCHLIST";
export const REMOVE_FROM_WATCHLIST = "REMOVE_FROM_WATCHLIST";
export const START_LOADING_WATCHLIST_SYMBOL = "START_LOADING_WATCHLIST_SYMBOL";
export const FINISH_LOADING_WATCHLIST_SYMBOL =
  "FINISH_LOADING_WATCHLIST_SYMBOL";
export const RESET = "RESET";

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
    portfolio: {
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
    notifications: [],
    is_loading: true,
  },
  stocks: { data: [], dict: {}, is_loading: true },
  is_loading: {
    user: { watchlist: new Set() },
  },
};

/*
  REDUCERS
*/
const user = (state = initialState.user, action) => {
  switch (action.type) {
    case UPDATE_USER:
      return { ...action.user, is_loading: false };
    case UPDATE_ORDERS:
      return { ...state, orders: action.orders };
    case UPDATE_WATCHLIST:
      return { ...state, watchlist: action.watchlist };
    case ADD_TO_WATCHLIST:
      const watchlist_added = [...state.watchlist, action.stock];
      watchlist_added.sort((a, b) => (a.symbol > b.symbol ? 1 : -1));
      return { ...state, watchlist: watchlist_added };
    case REMOVE_FROM_WATCHLIST:
      const watchlist_removed = state.watchlist.filter(
        (stock) => stock.symbol !== action.symbol
      );
      return { ...state, watchlist: watchlist_removed };
    case RESET:
      return initialState.user;
    default:
      return state;
  }
};

const stocks = (state = initialState.stocks, action) => {
  switch (action.type) {
    case UPDATE_STOCKS:
      const data = action.stocks;
      const dict = data.reduce((acc, stock) => {
        acc[stock.symbol] = stock;
        return acc;
      }, {});
      return { data, dict, is_loading: false };
    case RESET:
      return initialState.stocks;
    default:
      return state;
  }
};

const is_loading = (state = initialState.is_loading, action) => {
  switch (action.type) {
    case START_LOADING_WATCHLIST_SYMBOL:
      const watchlist_added = new Set(state.user.watchlist);
      watchlist_added.add(action.symbol);
      return { ...state, user: { ...state.user, watchlist: watchlist_added } };
    case FINISH_LOADING_WATCHLIST_SYMBOL:
      const watchlist_removed = new Set(state.user.watchlist);
      watchlist_removed.delete(action.symbol);
      return {
        ...state,
        user: { ...state.user, watchlist: watchlist_removed },
      };
    case RESET:
      return initialState.is_loading;
    default:
      return state;
  }
};

export default combineReducers({ user, stocks, is_loading });

/*
  SELECTORS
*/
const getPortfolio = (state) => state.user.portfolio;
const getWatchlist = (state) => state.user.watchlist;
const getStocks = (state) => state.stocks;
export const getStockBySymbol = (symbol) => (state) =>
  state.stocks.dict[symbol];
export const isSymbolInWatchlist = (symbol) => (state) =>
  getWatchlist(state).findIndex((x) => x.symbol === symbol) !== -1;

export const isSymbolInWatchlistLoading = (symbol) => (state) =>
  state.is_loading.user.watchlist.has(symbol);

const getNotifsReversed = (state) => state.user.notifications;

export const getNotifs = createSelector([getNotifsReversed], (revNotifs) =>
  [...revNotifs].reverse()
);

const getTransactionsReversed = (state) => state.user.transactions;

export const getTransactions = createSelector(
  [getTransactionsReversed],
  (revTransactions) => [...revTransactions].reverse()
);

export const getTransactionsForSymbol = (symbol) =>
  createSelector([getTransactionsReversed], (revTransactions) =>
    revTransactions.filter((t) => t.symbol === symbol).reverse()
  );

const getOrdersReversed = (state) => state.user.orders;

export const getOrders = createSelector([getOrdersReversed], (revOrders) => {
  return [...revOrders].reverse();
});

export const getOrdersForSymbol = (symbol) =>
  createSelector([getOrdersReversed], (revOrders) =>
    revOrders.filter((t) => t.symbol === symbol).reverse()
  );

export const getPortfolioRealTimeData = createSelector(
  [getPortfolio, getStocks],
  ({ long, short }, stocks) => {
    return {
      long: long.map((x) => stocks.dict[x.symbol]),
      short: short.map((x) => stocks.dict[x.symbol]),
    };
  }
);

export const getWatchlistRealTimeData = createSelector(
  [getWatchlist, getStocks],
  (watchlist, stocks) => watchlist.map((x) => stocks.dict[x.symbol])
);

/*
  ACTION CREATORS
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

export const initState = makeActionCreator(UPDATE);
export const resetState = makeActionCreator(RESET);
const updateUser = makeActionCreator(UPDATE_USER, "user");
const updateStocks = makeActionCreator(UPDATE_STOCKS, "stocks");
const updateWatchlist = makeActionCreator(UPDATE_WATCHLIST, "watchlist");
const updateOrders = makeActionCreator(UPDATE_ORDERS, "orders");
const addToWatchlistSync = makeActionCreator(ADD_TO_WATCHLIST, "stock");
const removeFromWatchlistSync = makeActionCreator(
  REMOVE_FROM_WATCHLIST,
  "symbol"
);
const startLoadingWatchlistSymbol = makeActionCreator(
  START_LOADING_WATCHLIST_SYMBOL,
  "symbol"
);
const finishLoadingWatchlistSymbol = makeActionCreator(
  FINISH_LOADING_WATCHLIST_SYMBOL,
  "symbol"
);

/*
  ACTIONS
*/
function reloadFromAPI(endpoint, updateFn) {
  return function(dispatch) {
    axios
      .get(endpoint)
      .then(
        (response) => dispatch(updateFn(response.data)),
        (error) => console.log("ERROR reloading from " + endpoint)
      )
      .finally(() => {
        !auth.currentUser && dispatch(resetState());
      });
  };
}

export const reloadUser = reloadFromAPI("/user/detail", updateUser);
export const reloadStocks = reloadFromAPI(
  "/stocks/real_time/all",
  updateStocks
);

export const reloadAll = (dispatch) => {
  dispatch(reloadUser);
  dispatch(reloadStocks);
};

export function addToWatchlistWithSnack(symbol, handleSnack) {
  return function(dispatch, getState) {
    const stock = getState().stocks.dict[symbol];
    dispatch(startLoadingWatchlistSymbol(symbol));
    dispatch(addToWatchlistSync(stock));
    handleSnack(`/watchlist?symbol=${symbol}`, "post")
      .then((response) => {
        dispatch(updateWatchlist(response.data));
      })
      .catch((error) => console.log(error))
      .finally(() =>
        auth.currentUser
          ? dispatch(finishLoadingWatchlistSymbol(symbol))
          : dispatch(resetState())
      );
  };
}

export function removeFromWatchlistWithSnack(symbol, handleSnack) {
  return function(dispatch) {
    dispatch(startLoadingWatchlistSymbol(symbol));
    dispatch(removeFromWatchlistSync(symbol)); // makes the change visible quickly
    handleSnack(`/watchlist?symbol=${symbol}`, "delete")
      .then((response) => dispatch(updateWatchlist(response.data)))
      .catch((error) => console.log(error))
      .finally(() =>
        auth.currentUser
          ? dispatch(finishLoadingWatchlistSymbol(symbol))
          : dispatch(resetState())
      );
  };
}

export function removeFromOrdersWithSnack(id, handleSnack) {
  return function(dispatch) {
    handleSnack(`/orders?id=${id}`, "delete")
      .then((response) => dispatch(updateOrders(response.data)))
      .catch((error) => console.log(error))
      .finally(() => {
        !auth.currentUser && dispatch(resetState());
      });
  };
}
