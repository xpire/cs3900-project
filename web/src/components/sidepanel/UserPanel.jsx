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
      <Typography>${format(stats.total_value)}</Typography>
      {/* Other values */}
      <Divider />
      <Grid container>
        {items.map(({ id, label }) =>
          HalfGridItem({ label: label, value: stats[id] })
        )}
      </Grid>
    </div>
  );

  return <ScrollPanel title={title} content={content} addPadding={false} />;
}

export default UserPanel;
