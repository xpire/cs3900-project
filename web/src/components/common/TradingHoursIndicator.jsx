import React from "react";
import PropTypes from "prop-types";
import { Chip, Tooltip } from "@material-ui/core";
import OfflineIcon from "@material-ui/icons/NightsStay";
import OnlineIcon from "@material-ui/icons/Brightness4";

/**
 * A Chip component which indicates whether Trading Hours are currently open
 */
const TradingHoursIndicator = ({ online }) => {
  return (
    <Tooltip
      title={
        online
          ? "Currently Trading hours are Open"
          : "Currently Trading hours are Closed"
      }
      aria-label="trading-hours"
    >
      <Chip
        size="small"
        variant="outlined"
        color={online ? "primary" : "default"}
        icon={online ? <OnlineIcon /> : <OfflineIcon />}
        label={online ? "Open" : "Closed"}
      />
    </Tooltip>
  );
};

TradingHoursIndicator.propTypes = {
  online: PropTypes.bool,
};

export default TradingHoursIndicator;
