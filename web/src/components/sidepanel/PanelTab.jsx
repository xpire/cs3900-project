import React, { useState } from "react";
import { Tabs, Tab } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";
import { Spacing } from "./Common";
import ScrollPanel from "./ScrollablePanel";

const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: "50px",
  },
}));

export function PanelTab({ tab1, tab2 }) {
  const classes = useStyles();
  const [tab, setTab] = useState(0);

  const subtitle = tab === 0 ? tab1.subtitle : tab2.subtitle;
  const content = tab === 0 ? tab1.content : tab2.content;

  const title = (
    <>
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
      {subtitle}
    </>
  );
  return <ScrollPanel title={title} content={content} />;
}
