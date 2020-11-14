import React from "react";
import { Typography } from "@material-ui/core";

import { format } from "../../utils/formatter";
import { useSelector } from "react-redux";
import { PanelTab } from "./PanelTab";

function PortfolioTable({ data }) {
  return (
    <div>
      {data.map(({ symbol, owned, price }) => {
        return (
          <Typography>
            {symbol + " qty:" + owned + " $" + format(price)}
          </Typography>
        );
      })}
    </div>
  );
}

function PortfolioPanel() {
  const { long, short } = useSelector((state) => state.user.portfolio);

  const tab1 = { label: "Longs", content: <PortfolioTable data={long} /> };
  const tab2 = { label: "Shorts", content: <PortfolioTable data={short} /> };

  return <PanelTab tab1={tab1} tab2={tab2} />;
}

export default PortfolioPanel;
