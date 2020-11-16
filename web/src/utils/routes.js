import React from "react";
// public
import HomePage from "../routes/Home/HomePage";
import HomeIcon from "@material-ui/icons/Home";
import LoginPage from "../routes/Auth/LoginPage";
import LoginIcon from "@material-ui/icons/LockOpen";
import SignUpPage from "../routes/Auth/SignUpPage";
import SignUpIcon from "@material-ui/icons/Lock";
import ForgotPasswordPage from "../routes/Auth/ForgotPasswordPage";
import ForgotPasswordIcon from "@material-ui/icons/VpnKey";
// private
import DashboardPage from "../routes/Dashboard/DashboardPage";
import DashboardIcon from "@material-ui/icons/Dashboard";
import PortfolioPage from "../routes/Portfolio/PortfolioPage";
import PortfolioIcon from "@material-ui/icons/TrackChanges";
import WatchlistPage from "../routes/Watchlist/WatchlistPage";
import WatchlistIcon from "@material-ui/icons/ViewList";
import MarketPage from "../routes/Market/MarketPage";
import MarketIcon from "@material-ui/icons/TrendingUp";
import OrderPage from "../routes/Orders/OrdersPage";
import OrderIcon from "@material-ui/icons/MenuBook";
import StockDetailsPage from "../routes/StockDetails/StockDetailsPage";
import StockDetailsIcon from "@material-ui/icons/Assessment";
import ProfilePage from "../routes/Profile/ProfilePage";
import ProfileIcon from "@material-ui/icons/AccountCircle";
import LeaderboardPage from "../routes/Leaderboard/LeaderboardPage";
import LeaderboardIcon from "@material-ui/icons/BarChart";
import SupportPage from "../routes/Support/SupportPage";
import SupportIcon from "@material-ui/icons/Help";

/**
 * An array of objects with the Structure: [
  {
    text: "Page Name",
    path: "page path",
    component: Page Component,
    icon: Page Icon,
    isPublic: Is this route available on public facing site? (not logged in),
    exact: Match this route exactly (no sub paths),
    isShown: Is this shown in sidebar?,
  },
]
 */
export const Routes = [
  {
    text: "Dashboard",
    path: "/home",
    component: DashboardPage,
    icon: <DashboardIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Portfolio",
    path: "/portfolio",
    component: PortfolioPage,
    icon: <PortfolioIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Watchlist",
    path: "/watchlist",
    component: WatchlistPage,
    icon: <WatchlistIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Market",
    path: "/market",
    component: MarketPage,
    icon: <MarketIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Stock",
    path: "/stock/:symbol",
    component: StockDetailsPage,
    icon: <StockDetailsIcon />,
    isPublic: false,
    exact: false,
    isShown: false,
  },
  {
    text: "Orders",
    path: "/orders",
    component: OrderPage,
    icon: <OrderIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Profile",
    path: "/profile",
    component: ProfilePage,
    icon: <ProfileIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Rankings",
    path: "/leaderboard",
    component: LeaderboardPage,
    icon: <LeaderboardIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Support",
    path: "/support",
    component: SupportPage,
    icon: <SupportIcon />,
    isPublic: false,
    exact: false,
    isShown: true,
  },
  {
    text: "Home",
    path: "/",
    component: HomePage,
    icon: <HomeIcon />,
    isPublic: true,
    exact: true,
    isShown: true,
  },
  {
    text: "Sign In",
    path: "/signin",
    component: LoginPage,
    icon: <LoginIcon />,
    isPublic: true,
    exact: false,
    isShown: true,
  },
  {
    text: "Sign Up",
    path: "/signup",
    component: SignUpPage,
    icon: <SignUpIcon />,
    isPublic: true,
    exact: false,
    isShown: true,
  },
  {
    text: "Forgot",
    path: "/forgot",
    component: ForgotPasswordPage,
    icon: <ForgotPasswordIcon />,
    isPublic: true,
    exact: false,
    isShown: true,
  },
];

export const locationToRoutes = Routes.reduce(
  (acc, cur) => ({ ...acc, [cur.path.match(/^\/[^/]*/)]: cur.text }),
  {}
);
