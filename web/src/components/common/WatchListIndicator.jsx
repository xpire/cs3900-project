import React, { useEffect, useMemo } from "react";
import { Button } from "@material-ui/core";
import VisibilityIcon from "@material-ui/icons/Visibility";
import VisibilityOffIcon from "@material-ui/icons/VisibilityOff";
import {
  isSymbolInWatchlist,
  addToWatchlistWithSnack,
  removeFromWatchlistWithSnack,
  isSymbolInWatchlistLoading,
} from "../../reducers";
import { useSelector, useDispatch } from "react-redux";
import useHandleSnack from "../../hooks/useHandleSnack";

const WatchListIndicator = ({ symbol }) => {
  const dispatch = useDispatch();
  const handleSnack = useHandleSnack(true);

  const watched = useSelector(isSymbolInWatchlist(symbol), (a, b) => a == b);
  const is_loading = useSelector(isSymbolInWatchlistLoading(symbol));

  return !watched ? (
    <Button
      size="small"
      color="primary"
      startIcon={<VisibilityIcon />}
      onClick={() =>
        !is_loading && dispatch(addToWatchlistWithSnack(symbol, handleSnack))
      }
    >
      watch
    </Button>
  ) : (
    <Button
      size="small"
      style={{
        color: "#ef5350",
      }}
      startIcon={<VisibilityOffIcon />}
      onClick={() =>
        !is_loading &&
        dispatch(removeFromWatchlistWithSnack(symbol, handleSnack))
      }
    >
      un-watch
    </Button>
  );
};

export default React.memo(WatchListIndicator);
