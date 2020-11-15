import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@material-ui/core";

import { StyledMarkdown } from "../components/common/styled";
import tutorialStats from "./understanding_stats.md.js";
import tutorialMarket from "./market_orders.md.js";
import tutorialAfter from "./after_market_orders.md.js";
import tutorialLimit from "./limit_orders.md.js";
import tutorialShortCover from "./shorts_and_covers.md.js";
import tutorialLevelingUp from "./leveling_up.md.js";
import tutorialStockGraph from "./stock_graph.md.js";

export const tutorials = [
  {
    body: tutorialStats,
    title: "Understanding Portfolio Statistics",
    unlock: 1,
  },
  { body: tutorialMarket, title: "Market Orders", unlock: 1 },
  { body: tutorialLevelingUp, title: "Leveling Up", unlock: 1 },
  { body: tutorialStockGraph, title: "Stock Graphs", unlock: 1 },
  { body: tutorialAfter, title: "After Market Orders", unlock: 2 },
  { body: tutorialLimit, title: "Limit Orders", unlock: 3 },
  {
    body: tutorialShortCover,
    title: "Short Selling and Buying to Cover",
    unlock: 5,
  },
];

const TutorialDialog = ({ open, title, body, handleClose }) => {
  return (
    <Dialog open={open} onClose={handleClose} scroll="body">
      <DialogTitle id="scroll-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText
        //   id="scroll-dialog-description"
        //   tabIndex={-1}
        >
          <StyledMarkdown>{body}</StyledMarkdown>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          OK
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default TutorialDialog;
