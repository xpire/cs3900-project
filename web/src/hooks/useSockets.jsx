import { useState, useEffect } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import app from "../utils/firebase";

// import { AuthContext } from "../utils/authentication";
import { useAuthState } from "react-firebase-hooks/auth";

const useSockets = () => {
  const socketUrl = "ws://localhost:8000/user/notifs";
  const [user] = useAuthState(app.auth());
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
    socketUrl,
    {
      onOpen: () => console.log("useSockets: opened"),
      onClose: () => console.log("useSockets: closed"),
      onMessage: () => console.log("useSockets: onMessage"),
      onError: () => console.log("useSockets: onError"),
      // will attempt to reconnect on all close events, such as server shutting down
      shouldReconnect: (closeEvent) => true,
      retryOnError: true,
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
    console.log({ readyState, user });
    if (readyState === ReadyState.OPEN) {
      user &&
        user.emailVerified &&
        user
          .getIdToken()
          .then((token) => {
            console.log(`I am sending token now: ${token}`);
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

  return [lastJsonMessage, messageHistory, connectionStatus];
};

export default useSockets;
