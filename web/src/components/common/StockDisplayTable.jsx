import React, { useEffect, useState } from "react";
import { Tooltip } from "@material-ui/core";
import Divider from '@material-ui/core/Divider';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';


const StockDisplayTable = ({name, exchange, industry, currency, type, fullname, renderStatus}) => {
    const displayValues = {
      "Full Name": name, 
      "Exchange": exchange, 
      "Industry": industry, 
      "Currency": currency, 
      "Type":type
    }

  return Object.keys(displayValues).map((key) => {
    return (
      <div key={key + "_div"}>
      <ListItem key={key} style={{padding: "4px 0px"}}>
        <ListItemText primary={key} style={{float: "left", color: "grey"}}/> 

          {key !== "Full Name" ? (
              <ListItemSecondaryAction style={{  
                position: "absolute", 
                right: "0px"
              }}>
                <ListItemText primary={displayValues[key]} color="secondary"/>
              </ListItemSecondaryAction>
            ) : (
              renderStatus ? (              
                  <ListItemSecondaryAction style={{  
                    position: "absolute", 
                    right: "0px"
                  }}>
                    <ListItemText primary={displayValues[key]}/>
                  </ListItemSecondaryAction>
                ) : (
                  <Tooltip
                  title={fullname == undefined ? "placeholder" : fullname}>
                  <ListItemSecondaryAction style={{  
                position: "absolute", 
                right: "0px"
              }}>
                    <ListItemText primary={displayValues[key]}/>
                  </ListItemSecondaryAction>
                </Tooltip>
              ))}
      </ListItem>
      <Divider variant="inset" component="li" style={{padding: "0"}}/>
      </div>
    )
  })
}


export default StockDisplayTable;