import React from "react";
import { useSnackbar } from "notistack";
import DetailedSnackbar from "../components/common/DetailedSnackbar";

const useHandleSocketSnack = (setCelebration) => {
  const { enqueueSnackbar } = useSnackbar();
  return (lastJsonMessage) => {
    console.log(`Inside handleSnack: ${JSON.stringify(lastJsonMessage)}`);
    switch (lastJsonMessage?.type) {
      case "auth":
        enqueueSnackbar(`${lastJsonMessage.msg}`, {
          variant: "info",
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
      default:
    }
  };
};

export default useHandleSocketSnack;
