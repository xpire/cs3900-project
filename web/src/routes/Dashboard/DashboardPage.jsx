import React, { useContext, useState, useEffect } from "react";
import { Typography, Tab, Tabs, Grid } from "@material-ui/core";

import { AuthContext } from "../../utils/authentication";
import Page from "../../components/page/Page";
import { StandardCard, ColoredText } from "../../components/common/styled";
import CardGrid from "../../components/common/CardGrid";
import ApexCandlestick from "../../components/graph/ApexCandlestick";
import axios from "../../utils/api";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";

import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call
// import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

// const stockData = data.data; //.slice(0, 30);

const parsedApexData = TimeSeriesData.AAPL.values
  .map(({ datetime, open, close, high, low }) => {
    return { x: new Date(datetime), y: [open, high, low, close] };
  })
  .slice(0, 120);

const StatCard = ({ name, value, stat, today }) => {
  return (
    <StandardCard style={{ minHeight: "130px" }}>
      {/* TODO: make this not hardcoded somehow */}
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item xs={12} container>
          <Typography variant="button">{name}</Typography>
        </Grid>
        <Grid item container alignItems="flex-end" spacing={1}>
          <Grid item>
            <Typography variant="h4">{value}</Typography>
          </Grid>
          {stat && (
            <Grid item>
              <ColoredText color={stat > 0 ? "green" : "red"} variant="h5">
                ({stat})
              </ColoredText>
            </Grid>
          )}
        </Grid>
        {today && (
          <>
            <Grid item xs={12}>
              <Typography variant="caption">Today:</Typography>
            </Grid>
            <Grid item xs={12}>
              <ColoredText
                variant="subtitle2"
                color={stat > 0 ? "green" : "red"}
              >
                {today}
              </ColoredText>
            </Grid>
          </>
        )}
      </Grid>
    </StandardCard>
  );
};

const StatisticsData = [
  { name: "Portfolio Value", value: 21123.33, stat: 5.3, today: -1.4 },
  { name: "Net Value", value: 26992.23, stat: 23, today: 2 },
  { name: "Profit", value: 1992.23, stat: 4.3, today: 10.4 },
  // { name: "Available Balance", value: 5001.22 },
];

// const TabPanel = (props) => {
//   const { children, value, index, ...other } = props;

//   return (
//     <div
//       role="tabpanel"
//       hidden={value !== index}
//       key={index}
//       id={`simple-tabpanel-${index}`}
//       aria-labelledby={`simple-tab-${index}`}
//       {...other}
//     >
//       {value === index && (
//         <Box p={3}>
//           <Typography>{children}</Typography>
//         </Box>
//       )}
//     </div>
//   );
// };

// const longsData = stockData.slice(0, 3);
// const shortsData = stockData.slice(3, 6);
// const watchData = stockData.slice(3, 9);

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  console.log(user.getIdToken(true));
  const [myValue, setValue] = useState(0);
  const [stockData, loading] = useRealTimeStockData();

  const [data, setData] = useState(
    stockData.slice(myValue * 3, myValue * 3 + 3)
  );

  useEffect(() => {
    setData(stockData.slice(myValue * 3, myValue * 3 + 3));
  }, [myValue, stockData]);

  const [balance, setBalance] = useState(0);

  const getBalance = () => {
    axios
      .get("/user/balance")
      .then((response) => {
        setBalance(response.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    user &&
      user
        .getIdToken()
        .then((token) => {
          getBalance(token);
        })
        .catch((e) => {});
  }, [user]);

  const balance_card = { name: "Available Balance", value: balance };

  return (
    <Page>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        {StatisticsData.map((data, index) => (
          <Grid key={index} item md={3} sm={6} xs={12}>
            <StatCard {...data} />
          </Grid>
        ))}
        <Grid key={4} item md={3} sm={6} xs={12}>
          <StatCard {...balance_card} />
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <ApexCandlestick data={parsedApexData} />
          </StandardCard>
        </Grid>
        <Grid item xs={12}>
          <StandardCard>
            <Tabs
              value={myValue}
              onChange={(_event, newValue) => {
                console.log("setting value to", newValue);
                setValue(newValue);
                setData(stockData.slice(myValue * 3, myValue * 3 + 3));
              }}
              indicatorColor="primary"
              textColor="primary"
              variant="fullWidth"
            >
              <Tab label="Longs" />
              <Tab label="Shorts" />
              <Tab label="Watchlist" />
            </Tabs>
          </StandardCard>
          <CardGrid data={data} />
        </Grid>
      </Grid>
    </Page>
  );
};

export default Dashboard;
