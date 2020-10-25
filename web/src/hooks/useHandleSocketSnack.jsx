import { useSnackbar } from "notistack";

const useHandleSocketSnack = () => {
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
        if (lastJsonMessage.msg.event_type === `LEVEL_UP`) {
          enqueueSnackbar(`${lastJsonMessage.msg.title}`, {
            variant: "success",
          });
        } else if (lastJsonMessage.msg.event_type === `ACHIEVEMENT_UNLOCKED`) {
          enqueueSnackbar(
            `${lastJsonMessage.msg.title} (${lastJsonMessage.msg.content}xp)`,
            {
              variant: "success",
            }
          );
        } else {
          enqueueSnackbar(`${JSON.stringify(lastJsonMessage)}`, {
            variant: "success",
          });
        }

        break;
      default:
    }
  };
};

export default useHandleSocketSnack;
