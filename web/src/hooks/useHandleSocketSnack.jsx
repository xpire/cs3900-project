import React from "react";
import { useSnackbar } from "notistack";
import DetailedSnackbar from "../components/common/DetailedSnackbar";

let msg_id = 0;

const useHandleSocketSnack = (setCelebration) => {
  const { enqueueSnackbar } = useSnackbar();
  return (lastJsonMessage) => {
    switch (lastJsonMessage?.type) {
      case "auth":
        enqueueSnackbar(`${lastJsonMessage.msg}`, {
          variant: "info",
          preventDuplicate: true,
          key: `${lastJsonMessage.msg}`,
        });
        break;
      case "generic":
        msg_id++;
        const msg = lastJsonMessage.msg["title"];
        enqueueSnackbar(`${msg}`, {
          variant: "success",
          preventDuplicate: false,
          key: msg_id,
        });
        break;
      case "notif":
        enqueueSnackbar(lastJsonMessage.msg, {
          variant: "success",
          content: (key, message) => (
            <DetailedSnackbar
              id={key}
              message={message}
              celebrate={setCelebration}
            />
          ),
        });
        break;
      // case "orders": //TODO: limit order executed notification
      default:
    }
  };
};

export default useHandleSocketSnack;
