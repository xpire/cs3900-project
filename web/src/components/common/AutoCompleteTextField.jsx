import React, { useState, useEffect } from "react";
import axios from "../../utils/api";
import { TextField, CircularProgress } from "@material-ui/core";
import { Autocomplete } from "@material-ui/lab";

// import TradingHoursIndicator from "../../components/common/TradingHoursIndicator";

const AutoCompleteTextField = ({ value, setValue }) => {
  const [open, setOpen] = useState(false);
  const [options, setOptions] = useState([]);
  const loading = open && options.length === 0;

  useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }

    axios
      .get("/stocks")
      .then((resp) => {
        setOptions(resp.data.map(({ symbol }) => symbol));
      })
      .catch((err) => console.log("err", err));

    return () => {
      active = false;
    };
  }, [loading]);

  useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);
  return (
    <Autocomplete
      open={open}
      onOpen={() => {
        setOpen(true);
      }}
      onClose={() => {
        setOpen(false);
      }}
      onChange={(_event, newValue) => {
        setValue(newValue);
      }}
      autoHighlight
      value={value}
      getOptionSelected={(option, value) => option === value.name}
      getOptionLabel={(option) => option}
      options={options}
      loading={loading}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Symbol"
          variant="outlined"
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <React.Fragment>
                {loading ? (
                  <CircularProgress color="inherit" size={20} />
                ) : null}
                {params.InputProps.endAdornment}
              </React.Fragment>
            ),
            // startAdornment: (
            //   <InputAdornment position="start">
            //     <TradingHoursIndicator online={true} />
            //   </InputAdornment>
            // ),
          }}
        />
      )}
    />
  );
};

export default AutoCompleteTextField;
