import React, { useEffect, useState } from "react";
import { Tooltip, Typography } from "@material-ui/core";
import {
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from "@material-ui/core";
// import Divider from '@material-ui/core/Divider';
// import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
// import ListItem from '@material-ui/core/ListItem';
// import ListItemText from '@material-ui/core/ListItemText';

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
        <>
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
          <Divider />
        </>
      ))}
    </>
  );
  // return Object.keys(displayValues).map((key) => {
  //   return (
  //     <div key={key + "_div"}>
  //     <ListItem key={key} style={{padding: "4px 0px"}}>
  //       <ListItemText primary={key} style={{float: "left", color: "grey"}}/>

  //         {key !== "Full Name" ? (
  //             <ListItemSecondaryAction style={{
  //               position: "absolute",
  //               right: "0px"
  //             }}>
  //               <ListItemText primary={displayValues[key]} color="secondary"/>
  //             </ListItemSecondaryAction>
  //           ) : (
  //             renderStatus ? (
  //                 <ListItemSecondaryAction style={{
  //                   position: "absolute",
  //                   right: "0px"
  //                 }}>
  //                   <ListItemText primary={displayValues[key]}/>
  //                 </ListItemSecondaryAction>
  //               ) : (
  //                 <Tooltip
  //                 title={fullname == undefined ? "placeholder" : fullname}>
  //                 <ListItemSecondaryAction style={{
  //               position: "absolute",
  //               right: "0px"
  //             }}>
  //                   <ListItemText primary={displayValues[key]}/>
  //                 </ListItemSecondaryAction>
  //               </Tooltip>
  //             ))}
  //     </ListItem>
  //     <Divider variant="inset" component="li" style={{padding: "0"}}/>
  //     </div>
  //   )
  // })
};

export default StockDisplayTable;

/*
const StockFieldItem = (label) => {
  return (
    <ListItemSecondaryAction
      style={{
        position: "absolute",
        right: "0px",
      }}
    >
      <ListItemText primary={label} color="secondary" />
    </ListItemSecondaryAction>
  );
};

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
        <>
          <List>
            <ListItem key={key} style={{ padding: "4px 0px" }}>
              <Typography variant="caption" color="textSecondary">
                {key}
              </Typography>

              {key !== "Full Name" || renderStatus ? (
                <StockFieldItem label={displayValues[key]} />
              ) : (
                <Tooltip
                  title={fullname == undefined ? "placeholder" : fullname}
                >
                  <StockFieldItem label={displayValues[key]} />
                </Tooltip>
              )}
            </ListItem>
          </List>
          <Divider />
        </>
      ))}
    </>
  );
  */
