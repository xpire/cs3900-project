import React from "react";
import {
  Divider,
  Grid,
  Typography,
  Tooltip,
  LinearProgress,
} from "@material-ui/core";

import { format } from "../../utils/formatter";
import { useSelector } from "react-redux";
import { HalfGridItem, Spacing } from "./Common";
import ScrollPanel from "./ScrollablePanel";
import { auth } from "../../utils/authentication";

function UserPanel() {
  /* CAN BE MADE INTO FLOATING, BY USING AN INTERNAL CARD*/
  const {
    basic,
    stats,
    leaderboard: { user_ranking },
  } = useSelector((state) => state.user);

  let expPercentage = 0;
  if (basic.exp_threshold !== null && basic.exp_threshold > 0) {
    expPercentage = (basic.exp / basic.exp_threshold) * 100;
  }

  const items = [
    {
      id: "balance",
      label: "Balance",
      tooltip: "Your cash",
      pre: (x) => x,
    },
    {
      id: "total_long_value",
      label: "Long Value",
      tooltip: "Total value of your longs",
      pre: (x) => x,
    },
    {
      id: "short_balance",
      label: "Short Balance",
      tooltip: "How much more you can spend to short",
      pre: (x) => (x <= 0 ? 0 : x),
    },
    {
      id: "total_short_value",
      label: "Short Value",
      tooltip: "Amount to pay to cover all of your shorts",
      pre: (x) => Math.abs(x),
    },
  ];

  const title = <Typography variant="h6">{basic.username}</Typography>;
  const content = (
    <div>
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
      <Typography>Lv. {basic.level} </Typography>
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
      <Tooltip title="Your whole account's value" placement="left-start">
        <Typography>${format(stats.total_value)}</Typography>
      </Tooltip>
      {/* Other values */}
      <Divider />
      <Grid container>
        {items.map(({ id, label, tooltip, pre }) => (
          <Tooltip title={tooltip} placement="left-start">
            {HalfGridItem({ label: label, value: pre(stats[id]) })}
          </Tooltip>
        ))}
      </Grid>
    </div>
  );

  return <ScrollPanel title={title} content={content} addPadding={false} />;
}

export default UserPanel;
