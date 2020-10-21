import React, { useContext, useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import {
  Typography,
  Card,
  Grid,
  LinearProgress,
  CardContent,
} from "@material-ui/core";

import useSockets from "../../hooks/useSockets";
import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard } from "../../components/common/styled";

const Achievements = () => {
  const { user } = useContext(AuthContext);

  // TODO: see if we can use wss://
  // const socketUrl = "ws://localhost:8000/user/notifs";

  // const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
  //   socketUrl,
  //   {
  //     onOpen: () => console.log("opened"),
  //     // will attempt to reconnect on all close events, such as server shutting down
  //     shouldReconnect: (closeEvent) => true,
  //     reconnectAttempts: 20,
  //     reconnectInterval: 3000,
  //     share: true,
  //   }
  // );

  // const connectionStatus = {
  //   [ReadyState.CONNECTING]: "Connecting",
  //   [ReadyState.OPEN]: "Open",
  //   [ReadyState.CLOSING]: "Closing",
  //   [ReadyState.CLOSED]: "Closed",
  //   [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  // }[readyState];

  // useEffect(() => {
  //   if (readyState === ReadyState.OPEN) {
  //     console.log(user.getIdToken(true));
  //     user &&
  //       user
  //         .getIdToken(true)
  //         .then((token) => {
  //           sendJsonMessage(token);
  //         })
  //         .catch((e) => console.log(e));
  //   }
  // }, [readyState, user]);

  // const [messageHistory, setMessageHistory] = useState([]);
  // useEffect(() => {
  //   console.log("Recieved message");
  //   console.log(lastJsonMessage);
  //   setMessageHistory([...messageHistory, lastJsonMessage]);

  //   if (readyState === ReadyState.OPEN && lastJsonMessage.is_error) {
  //     console.log("ERROR: " + lastJsonMessage.error_msg);
  //   }
  // }, [lastJsonMessage]);
  const [lastJsonMessage, messageHistory, connectionStatus] = useSockets();

  return (
    <Page>
      <StandardCard>
        <CardContent>
          <Typography variant="h2">{user.email}</Typography>
          <Typography>{`Level ${5}`}</Typography>
          <LinearProgress variant="determinate" value={40} />
        </CardContent>
      </StandardCard>
      <Typography>{`websocket status: ${connectionStatus}`}</Typography>
      <Typography>{`last json message: ${JSON.stringify(
        lastJsonMessage
      )}`}</Typography>

      <Grid container>
        {messageHistory.map((msg, idx) => (
          <Grid item key={idx}>
            <StandardCard>
              <CardContent>
                <span key={idx}>
                  {JSON.stringify(msg)} <br />
                </span>
              </CardContent>
            </StandardCard>
          </Grid>
        ))}
      </Grid>
    </Page>
  );
};

export default Achievements;
