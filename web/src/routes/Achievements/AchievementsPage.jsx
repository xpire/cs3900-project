import React, { useContext, useEffect, useState } from "react";
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
      share: true,
    }
  );

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

  const [messageHistory, setMessageHistory] = useState([]);
  useEffect(() => {
    console.log("Recieved message");
    console.log(lastJsonMessage);
    setMessageHistory([...messageHistory, lastJsonMessage]);

    if (readyState === ReadyState.OPEN && lastJsonMessage.is_error) {
      console.log("ERROR: " + lastJsonMessage.error_msg);
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

        <ul>
          {messageHistory.map((msg, idx) => (
            <span key={idx}>
              {JSON.stringify(msg)} <br />
            </span>
          ))}
        </ul>
      </Card>
    </Page>
  );
};

export default Achievements;
