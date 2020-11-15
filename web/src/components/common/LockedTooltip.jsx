import React from "react";
import { ToolTip, Tooltip } from "@material-ui/core";

const LockedTooltip = ({ children, userLevel, lockedLevel }) => {
  return (
    <Tooltip
      disableHoverListener={!userLevel || userLevel > lockedLevel}
      title={`Unlocked at level ${lockedLevel}`}
    >
      {children}
    </Tooltip>
  );
};

export default LockedTooltip;
