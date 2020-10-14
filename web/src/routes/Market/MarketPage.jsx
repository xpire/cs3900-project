import React, { useState } from "react";
import { Typography, Grid, Input } from "@material-ui/core";
import Page from "../../components/page/Page";
import StockCard from "../../components/common/StockCard";

import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

const toCard = ({ symbol, type, skeleton }, index) => {
  return (
    <Grid item md={4} sm={6} xs={12} key={index}>
      <StockCard
        name={symbol}
        category={type}
        price="$25,322"
        delta={index % 2 === 0 ? 25 : -10}
        key={index}
        skeleton={skeleton}
      />
    </Grid>
  );
};

const Market = () => {
  const [loading, setLoading] = useState(false);

  const stockData = data.data; //.slice(0, 30);
  const [filteredData, setFilteredData] = useState(stockData);

  const handleChange = (e) => {
    if (e !== "") {
      setFilteredData(
        stockData.filter(({ symbol }) =>
          symbol.toLowerCase().includes(e.toLowerCase())
        )
      );
    } else {
      setFilteredData(stockData);
    }
  };

  return (
    <Page>
      <div style={{ padding: "12px" }}>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
          spacing={2}
        >
          <Grid item xs={12}>
            <Input
              fullWidth
              onChange={(e) => handleChange(e.target.value)}
              variant="filled"
              placeholder="Search"
              inputProps={{ style: { fontSize: 40 } }}
            />
          </Grid>
          <Grid item xs={12}>
            <Typography>
              {loading
                ? `Loading...`
                : `Your search returned ${filteredData.length} results.`}
            </Typography>
          </Grid>
          {filteredData.map((stock, index) => toCard(stock, index))}
        </Grid>
      </div>
    </Page>
  );
};

export default Market;
