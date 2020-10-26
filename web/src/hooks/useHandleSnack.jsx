import { useSnackbar } from "notistack";
import axios from "../utils/api";

const useHandleSnack = () => {
  const { enqueueSnackbar } = useSnackbar();
  return async (path, method = "post") => {
    await axios
      .request({ url: path, method: method })
      .then((response) => {
        switch (response.status) {
          case 200:
            enqueueSnackbar(`${response.data.msg}`, {
              variant: "success",
            });
            break;
          default:
        }
      })
      .catch((err) => {
        console.log("handlesnack", err.response.status);
        switch (err.response.status) {
          case 400:
            enqueueSnackbar(`${err.response.data.detail}`, {
              variant: "warning", //"error",
            });
            break;
          case 500:
          default:
        }
      })
      .catch(() =>
        enqueueSnackbar(`Sorry, please try again.`, { variant: "error" })
      );
  };
};

export default useHandleSnack;
