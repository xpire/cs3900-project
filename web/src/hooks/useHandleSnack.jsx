import { useSnackbar } from "notistack";
import axios from "../utils/api";

const useHandleSnack = (ignore_success = false) => {
  const { enqueueSnackbar } = useSnackbar();
  return async (path, method = "post") => {
    return await axios
      .request({ url: path, method: method })
      .then((response) => {
        if (response.status === 200) {
          if (!ignore_success) {
            enqueueSnackbar(`${response.data.msg}`, {
              variant: "success",
            });
          }
          return response;
        }
      })
      .catch((err) => {
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
