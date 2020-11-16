import React, { useEffect, useState } from "react";
import { Tooltip, Typography } from "@material-ui/core";
import {
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from "@material-ui/core";

const StockDisplayTable = ({
  name,
  exchange,
  industry,
  currency,
  type,
  fullname,
  renderStatus,
}) => {
  const displayValues = {
    "Full Name": name,
    Exchange: exchange,
    Industry: industry,
    Currency: currency,
    Type: type,
  };

  return (
    <>
      <Divider />
      {Object.keys(displayValues).map((key) => (
        <div key={key + "_div"}>
          <List>
            <ListItem
              key={key}
              style={{ padding: "4px 0px" }}
              style={{ display: "block" }}
            >
              <Typography variant="caption" color="textSecondary">
                {key}
              </Typography>

              {key !== "Full Name" || renderStatus ? (
                <Typography>{displayValues[key]}</Typography>
              ) : (
                <Tooltip
                  title={fullname == undefined ? "placeholder" : fullname}
                >
                  <Typography>{displayValues[key]}</Typography>
                </Tooltip>
              )}
            </ListItem>
          </List>
          <Divider key={key} />
        </div>
      ))}
    </>
  );
};

export default StockDisplayTable;
