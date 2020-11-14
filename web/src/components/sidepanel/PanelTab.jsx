import React, { useState } from "react";
import { Tabs, Tab } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";
import { Spacing } from "./Common";

const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: "50px",
  },
}));

export function PanelTab({ tab1, tab2 }) {
  const classes = useStyles();
  const [tab, setTab] = useState(0);

  return (
    <div>
      <Tabs
        onChange={(_event, newValue) => {
          setTab(newValue);
        }}
        value={tab}
        indicatorColor="primary"
        textColor="primary"
        variant="fullWidth"
      >
        <Tab label={tab1.label} className={classes.root} />
        <Tab label={tab2.label} className={classes.root} />
      </Tabs>
      <Spacing />
      {tab === 0 ? tab1.content : tab2.content}
    </div>
  );
}
