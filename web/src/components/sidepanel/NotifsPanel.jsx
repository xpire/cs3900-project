import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Typography,
  makeStyles,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { getNotifs } from "../../reducers";
import { getIcon } from "../common/DetailedSnackbar";
import ScrollPanel from "./ScrollablePanel";

function NotifsPanel() {
  const notifs = useSelector(getNotifs);

  const title = <Typography variant="h6">Notifications</Typography>;
  const content = (
    <List>
      <Divider />
      {notifs.map(({ id, event_type, title }) => (
        <ListItem divider dense key={id}>
          <ListItemIcon>{getIcon(event_type)}</ListItemIcon>
          <ListItemText primary={title} />
        </ListItem>
      ))}
    </List>
  );
  return <ScrollPanel title={title} content={content} />;
}

export default NotifsPanel;
