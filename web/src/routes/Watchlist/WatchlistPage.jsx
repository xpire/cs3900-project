import React from "react";
import { Card } from "@material-ui/core";

import Page from "../../components/page/Page";
import SortableStockTable, {
  tableTypes,
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
  const dispatch = useDispatch();
  const handleSnack = useHandleSnack(true);
  const data = useSelector((state) => state.user.watchlist); // TODO add a selector that retrieves watchlist/orders with given stocks data
  const stocks = useSelector((state) => state.stocks.dict);
  const mappedData = data.map(({ exchange, name, symbol }) => {
    const price = stocks[symbol]?.curr_day_close || 0;
    const open = stocks[symbol]?.curr_day_open || 0;
    return {
      symbol: symbol,
      name: name,
      exchange: exchange,
      price: price,
      open: open,
      daily: format(price - open),
      dailyPercentage: format((100 * (price - open)) / open),
    };
  });
  return (
    <Page>
      <Card>
        <SortableStockTable
          data={mappedData}
          columns={columns}
          title="Watchlist"
          handleDelete={({ symbol }) =>
            dispatch(removeFromWatchlistWithSnack(symbol, handleSnack))
          }
        />
      </Card>
    </Page>
  );
};

export default Watchlist;
