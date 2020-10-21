import React, { useContext, useEffect } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { Typography, Card } from "@material-ui/core";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";

const Achievements = () => {
  const { user } = useContext(AuthContext);

  // TODO: see if we can use wss://
  const socketUrl = "ws://localhost:8000/user/notifs";

  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
    socketUrl,
    {
      onOpen: () => console.log("opened"),
      // will attempt to reconnect on all close events, such as server shutting down
      shouldReconnect: (closeEvent) => true,
      reconnectAttempts: 20,
      reconnectInterval: 3000,
    }
  );

  console.log("RERENDERED");

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  useEffect(() => {
    if (readyState === ReadyState.OPEN) {
      console.log(user.getIdToken(true));
      user &&
        user
          .getIdToken(true)
          .then((token) => {
            sendJsonMessage(token);
          })
          .catch((e) => console.log(e));
    }
  }, [readyState, user]);

  useEffect(() => {
    if (readyState === ReadyState.OPEN) {
      if (lastJsonMessage.is_error) {
        console.log("ERROR: " + lastJsonMessage.error_msg);
      } else if (lastJsonMessage.type === "auth") {
        // this was for testing purposes
        // sendJsonMessage(JSON.stringify({ name: "ian", desc: "cool" }));
      }
    }
  }, [lastJsonMessage]);

  return (
    <Page>
      <Card>
        <Typography variant="h2">Achievements Page</Typography>
        <Typography>{`Welcome ${user.email} to the Achievements page!`}</Typography>
        <Typography>{`websocket status: ${connectionStatus}`}</Typography>
        <Typography>{`last json message: ${JSON.stringify(
          lastJsonMessage
        )}`}</Typography>
      </Card>
    </Page>
  );
};

export default Achievements;
