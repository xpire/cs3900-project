import React, { useEffect, useState, useRef } from "react";
import PropTypes from "prop-types";
import {
  Button,
} from "@material-ui/core";
import VisibilityIcon from '@material-ui/icons/Visibility';
import useHandleSnack from "../../hooks/useHandleSnack";
import VisibilityOffIcon from '@material-ui/icons/VisibilityOff';

/**
 * Component to inidcate for watchlist
 */
const WatchListIndicator = ({ watchlistdata, symbol }) => {
  const handleSnack = useHandleSnack();
  const [watched, watchListClick] = watchlistdata; 

  return (
    !watched ? (
      <Button
      size="small"
      color="primary"
      startIcon={< VisibilityIcon />}
      onClick={() => {
        handleSnack(`/watchlist?symbol=${symbol}`, "post").then(() => watchListClick())
      }}
      >
          watch
        </Button >
    ) : (
      <Button
      size="small"
      // color="#ef5350"
      style = {{
        color: "#ef5350"
      }}
      startIcon={<VisibilityOffIcon />}
      onClick={() => {
        handleSnack(`/watchlist?symbol=${symbol}`, "delete").then(() => watchListClick())
        }}>
        un-watch
      </Button >
      )
  );
};


WatchListIndicator.propTypes = {
  /* Stores if the symbol is in the watchlist */
  exist: PropTypes.bool,
  /** Whether this card should display the Skeleton component to signify loading */
};

export default WatchListIndicator;
