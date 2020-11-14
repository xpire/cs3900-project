import React from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import { format } from "../../utils/formatter";
import { useDispatch, useSelector } from "react-redux";
import { removeFromWatchlist } from "../../reducers";

const headCells = [
  {
    id: "symbol",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Symbol",
  },
  {
    id: "name",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Name",
  },
  {
    id: "exchange",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Exchange",
  },
  {
    id: "price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Price",
  },
  {
    id: "open",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Open",
  },
  {
    id: "daily",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Day Change",
    color: true,
  },
  {
    id: "dailyPercentage",
    formatType: tableTypes.PERCENTAGE,
    disablePadding: false,
    label: "% Day Change",
    color: true,
  },
];

const Watchlist = () => {
  const dispatch = useDispatch();
  const data = useSelector((state) => state.user.watchlist); // TODO add a selector that retrieves watchlist/orders with given stocks data
  const mappedData = data.map(
    ({ curr_day_close, exchange, name, curr_day_open, symbol }) => {
      return {
        symbol: symbol,
        name: name,
        exchange: exchange,
        price: curr_day_close,
        open: curr_day_open,
        daily: format(curr_day_close - curr_day_open),
        dailyPercentage: format(
          (100 * (curr_day_close - curr_day_open)) / curr_day_open
        ),
      };
    }
  );

  return (
    <Page>
      <Card>
        <SortableTable
          data={mappedData}
          header={headCells}
          title="Watchlist"
          handleDelete={({ symbol }) => dispatch(removeFromWatchlist(symbol))}
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
