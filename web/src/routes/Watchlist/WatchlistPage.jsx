import React from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";
import useRealTimeStockData from "../../hooks/useRealTimeStockData";
import { format } from "../../utils/formatter";
import { useDispatch, useSelector } from "react-redux";
import { removeFromWatchlistWithSnack } from "../../reducers";
import useHandleSnack from "../../hooks/useHandleSnack";

const columns = [
  {
    field: "symbol",
    title: (
      <RenderItem
        title="Symbol"
        subtitle="Exchange/Name"
        alignItems="flex-start"
      />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.exchange}
        subtitleType={tableTypes.TEXT}
        subsubtitle={rowData.name}
        subsubtitleType={tableTypes.TEXT}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "price",
    title: <RenderItem title="Price" subtitle="Prev. Open" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.price}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.open}
        subtitleType={tableTypes.CURRENCY}
      />
    ),
    align: "right",
  },
  {
    field: "value",
    title: <RenderItem title="Daily" subtitle="%Daily" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.daily}
        titleType={tableTypes.CURRENCY}
        titleColor={true}
        subtitle={rowData.dailyPercentage}
        subtitleColor={true}
        subtitleType={tableTypes.PERCENTAGE}
      />
    ),
    align: "right",
  },
];

const Watchlist = () => {
  // // const [data, setData] = useState([]);
  // const [deleted, setDeleted] = useState(0);
  // const [data, loading, updateSymbols] = useRealTimeStockData(
  //   "/watchlist",
  //   [deleted],
  //   []
  // );
  const dispatch = useDispatch();
  const handleSnack = useHandleSnack(true);
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

  // const handleDelete = () => {
  //   console.log("watchist", deleted + 1);
  //   setDeleted(deleted + 1);
  //   console.log("watchist after", deleted + 1);
  // };

  return (
    <Page>
      <Card>
        <SortableStockTable
          data={mappedData}
          columns={columns}
          title="Watch List"
          // isLoading={loading}
          handleDelete={({ symbol }) => {
            dispatch(removeFromWatchlistWithSnack(symbol, handleSnack));
            // updateSymbols();
            // handleSnack(`/watchlist?symbol=${symbol}`, "delete").then(() =>
            // );
          }}
          // handleRefresh={handleDelete}
          // header={headCells}
          // title="Watchlist"
          // handleDelete={({ symbol }) =>
          //   dispatch(removeFromWatchlistWithSnack(symbol, handleSnack))
          // }
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
