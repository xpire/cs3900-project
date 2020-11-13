import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Typography,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { getIcon } from "../common/DetailedSnackbar";

function NotifsPanel() {
  const notifs = useSelector((state) => state.user.notifications);
  return (
    <div>
      <Typography>Notifications</Typography>
      <List>
        <Divider />
        {notifs.map((notif) => (
          <ListItem divider dense>
            <ListItemIcon>{getIcon(notif.event_type)}</ListItemIcon>
            <ListItemText primary={notif.title} />
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default NotifsPanel;
