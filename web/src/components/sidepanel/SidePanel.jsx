import React, { useState, useEffect } from "react";
import Drawer from "@material-ui/core/Drawer";
import {
  Divider,
  Grid,
  Toolbar,
  Box,
  Typography,
  Tooltip,
  LinearProgress,
} from "@material-ui/core";

import { reloadUser, UPDATE_USER } from "../../reducers/index";

import { format } from "../../utils/formatter";
import { useDispatch, useSelector } from "react-redux";

function HalfGridItem({ label, value }) {
  return (
    <Grid item xs={6}>
      <Typography
        variant="caption"
        color="textSecondary"
        style={{ fontSize: 11 }}
      >
        {label}
      </Typography>
      <Typography style={{ fontSize: 14 }}>${format(value)}</Typography>
    </Grid>
  );
}

function Spacing() {
  return <Box p={0.5} />;
}

function SidePanel({ classes }) {
  /* CAN BE MADE INTO FLOATING, BY USING AN INTERNAL CARD*/
  const {
    basic,
    stats,
    leaderboard: { user_ranking },
  } = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const [expPercentage, setExpPercentage] = useState(0);
  useEffect(() => {
    if (
      basic &&
      basic.exp_until_next_level &&
      basic.exp_until_next_level !== null
    ) {
      setExpPercentage((basic.exp / basic.exp_threshold) * 100);
    }
  }, [basic]);

  const items = [
    {
      id: "balance",
      label: "Balance",
    },
    {
      id: "total_long_value",
      label: "Long Value",
    },
    {
      id: "short_balance",
      label: "Short Balance",
    },
    {
      id: "total_short_value",
      label: "Short Value",
    },
  ];

  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
      anchor="right"
    >
      <Toolbar />
      <div className={classes.drawerContainer}>
        <div style={{ padding: "20px" }}>
          {/* Username */}
          <Typography variant="h6">{basic.username}</Typography>
          {/* Rank */}
          <Typography variant="caption" color="textSecondary">
            Rank
          </Typography>
          <Typography>{user_ranking}</Typography>
          {/* Level */}
          <Spacing />
          <Typography variant="caption" color="textSecondary">
            Level
          </Typography>
          <Typography display="span">Lv. {basic.level} </Typography>
          {/* <Typography color="textSecondary" display="span">
            
          </Typography> */}
          <Tooltip
            title={format(basic.exp) + "/" + basic.exp_threshold}
            placement="top-end"
          >
            <LinearProgress value={expPercentage} variant="determinate" />
          </Tooltip>
          {/* Networth */}
          <Spacing />
          <Typography variant="caption" color="textSecondary">
            Net Worth
          </Typography>
          <Typography>${format(stats.total_value)}</Typography>
          {/* Other values */}
          <Divider />
          <Grid container>
            {items.map(({ id, label }) =>
              HalfGridItem({ label: label, value: stats[id] })
            )}
          </Grid>
        </div>
      </div>
    </Drawer>
  );
}

export default SidePanel;

/*
shared data / or api response pool

api -> store and cache(?)
subscribe

if subscribed 
-> notification for update
-> call api for all subscribed...
*/

/*
Modified based on: https://stackoverflow.com/questions/53146795/react-usereducer-async-data-fetch
*/

/*
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
  watchlist: [],
  positions: [],
};

const GET_USER = "GET_USER";
// const WATCHLIST = "WATCHLIST";
// const RANKINGS = "RANKINGS";
const GET_STOCKS = "STOCKS";
const reducer = (state, action) => {
  switch (action.type) {
    case GET_USER:
      state = { ...state, user: { ...state.user, rank: state.user.rank + 1 } };
      break;
    case GET_STOCKS:
      break;
    default:
      throw new Error();
  }
};

// function isPromise(obj) {
//   return (
//     !!obj &&
//     (typeof obj === "object" || typeof obj === "function") &&
//     typeof obj.then === "function"
//   );
// }

// function asyncDispatchWrapper(dispatch) {
//   return function(action) {
//     if (isPromise(action.payload)) {
//       action.payload.then(v => {
//         dispatch({ type: action.type, payload: v });
//       });
//     } else {
//       dispatch(action);
//     }
//   };
// }

function DataStoreContextProvider({ children }) {
  const [user, setUser] = useState(0);
}

*/
