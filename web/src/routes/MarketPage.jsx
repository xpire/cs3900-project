import React, { useContext } from "react";
import { Typography, Card, Grid } from "@material-ui/core";

import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";
import StockCard from "../components/common/StockCard";

const Market = () => {
  const { user } = useContext(AuthContext);
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
            <Card>
              <Typography variant="h2">TODO: [Search bar]</Typography>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Typography>Your search returned 20 results.</Typography>
          </Grid>
          {[...Array(20).keys()].map((e) => {
            return (
              <Grid item md={4} sm={6} xs={12}>
                <StockCard
                  name="AAPL"
                  category="Technology"
                  price="$25,333"
                  delta={e % 2 === 0 ? 25 : -10}
                  key={e}
                />
              </Grid>
            );
          })}
        </Grid>
      </div>
    </Page>
  );
};

export default Market;
