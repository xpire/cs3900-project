import React from "react";
import { Chip, Tooltip } from "@material-ui/core";
import OfflineIcon from "@material-ui/icons/NightsStay";
import OnlineIcon from "@material-ui/icons/Brightness4";

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
        color={online ? "primary" : "default"}
        icon={online ? <OnlineIcon /> : <OfflineIcon />}
        label={online ? "Open" : "Closed"}
      />
    </Tooltip>
  );
};

export default TradingHoursIndicator;
