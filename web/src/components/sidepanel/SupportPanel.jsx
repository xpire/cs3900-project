import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { format } from "../../utils/formatter";
import ScrollPanel from "./ScrollablePanel";

function SupportPanel() {
  const title = <Typography variant="h6">Support</Typography>;
  const content = <Typography>Not implemented yet</Typography>;
  return <ScrollPanel title={title} content={content} addPadding={false} />;
}

export default SupportPanel;
