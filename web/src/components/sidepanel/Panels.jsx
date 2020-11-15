import React from "react";
import UserIcon from "@material-ui/icons/AccountCircle";
import NotifIcon from "@material-ui/icons/Notifications";
import OrderIcon from "@material-ui/icons/MenuBook";
import PortfolioIcon from "@material-ui/icons/TrackChanges";
import WatchlistIcon from "@material-ui/icons/Visibility";
import LeaderboardIcon from "@material-ui/icons/BarChart";
import SupportIcon from "@material-ui/icons/Help";
import UserPanel from "./UserPanel";
import PortfolioPanel from "./PortfolioPanel";
import OrdersPanel from "./OrdersPanel";
import NotifsPanel from "./NotifsPanel";
import WatchlistPanel from "./WatchlistPanel";
import LeaderboardPanel from "./LeaderboardPanel";
import SupportPanel from "./SupportPanel";

export const PANELS = [
  { name: "user", icon: <UserIcon />, panel: <UserPanel /> },
  { name: "notif", icon: <NotifIcon />, panel: <NotifsPanel /> },
  { name: "watchlist", icon: <WatchlistIcon />, panel: <WatchlistPanel /> },
  { name: "portfolio", icon: <PortfolioIcon />, panel: <PortfolioPanel /> },
  { name: "order", icon: <OrderIcon />, panel: <OrdersPanel /> },
  {
    name: "leaderboard",
    icon: <LeaderboardIcon />,
    panel: <LeaderboardPanel />,
  },
];

export const DEFAULT_PANEL_NAME = "user";
