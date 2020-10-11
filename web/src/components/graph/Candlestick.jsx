import React from "react";
import PropTypes from "prop-types";

import { green, red } from "../common/styled";

import { format } from "d3-format";
import { timeFormat } from "d3-time-format";

import { ChartCanvas, Chart } from "react-stockcharts";
import { CandlestickSeries } from "react-stockcharts/lib/series";
import { XAxis, YAxis } from "react-stockcharts/lib/axes";

import {
  CrossHairCursor,
  EdgeIndicator,
  MouseCoordinateX,
  MouseCoordinateY,
} from "react-stockcharts/lib/coordinates";
import {
  OHLCTooltip,
  // MovingAverageTooltip,
  // BollingerBandTooltip,
  // StochasticTooltip,
  // GroupTooltip,
} from "react-stockcharts/lib/tooltip";

import { discontinuousTimeScaleProvider } from "react-stockcharts/lib/scale";
import { fitWidth } from "react-stockcharts/lib/helper";

class CandleStickStockScaleChart extends React.Component {
  render() {
    const {
      type,
      data: initialData,
      width,
      ratio,
      leftEdge = false,
      rightYAxis = false,
      rightEdge = true,
    } = this.props;

    const xScaleProvider = discontinuousTimeScaleProvider.inputDateAccessor(
      (d) => d.date
    );
    const { data, xScale, xAccessor, displayXAccessor } = xScaleProvider(
      initialData
    );
    const xExtents = [
      xAccessor(data[data.length - 1]),
      xAccessor(data[data.length > 120 ? data.length - 120 : 0]),
    ];

    return (
      <ChartCanvas
        height={400}
        ratio={ratio}
        width={width}
        margin={{ left: 50, right: 50, top: 20, bottom: 30 }}
        type={type}
        data={data}
        xScale={xScale}
        xAccessor={xAccessor}
        displayXAccessor={displayXAccessor}
        xExtents={xExtents}
      >
        <Chart id={1} yExtents={(d) => [d.high, d.low]}>
          <XAxis
            axisAt="bottom"
            orient="bottom"
            ticks={6}
            tickStroke="#FFFFFF"
            stroke="#FFFFFF"
          />
          <YAxis
            axisAt="left"
            orient="left"
            ticks={5}
            tickStroke="#FFFFFF"
            stroke="#FFFFFF"
          />
          <MouseCoordinateX
            at="bottom"
            orient="bottom"
            displayFormat={timeFormat("%Y-%m-%d")}
          />
          <MouseCoordinateY
            at="right"
            orient="right"
            displayFormat={format(".2f")}
          />
          <CandlestickSeries
            stroke={(d) => (d.close > d.open ? green.dark : red.dark)} //"#6BA583" : "#DB0000")}
            wickStroke={(d) => (d.close > d.open ? green.dark : red.dark)} //"#6BA583" : "#DB0000")}
            fill={(d) => (d.close > d.open ? green.dark : red.dark)} //"#6BA583" : "#DB0000")}
          />

          {rightYAxis && (
            <YAxis
              axisAt="right" //"left"
              orient="right" //"left"
              ticks={5}
              tickStroke="#FFFFFF"
              stroke="#FFFFFF"
            />
          )}
          {rightEdge && (
            <EdgeIndicator
              itemType="last"
              orient="right"
              lineStroke="#FFFFFF"
              edgeAt="right"
              yAccessor={(d) => d.close}
              fill={(d) => (d.close > d.open ? green.light : red.dark)} //"#6BA583" : "#DB0000")}
            />
          )}
          {leftEdge && (
            <EdgeIndicator
              itemType="first"
              orient="left"
              lineStroke="#FFFFFF"
              edgeAt="left"
              yAccessor={(d) => d.close}
              fill={(d) => (d.close > d.open ? green.dark : red.dark)} //"#6BA583" : "#DB0000")}
            />
          )}
          <OHLCTooltip
            fontFamily="Roboto"
            fontSize="16px"
            textFill="#FFFFFF"
            labelFill="#2196f3"
            origin={[-50, -10]}
          />
        </Chart>
        <CrossHairCursor stroke="#FFFFFF" />
      </ChartCanvas>
    );
  }
}

CandleStickStockScaleChart.propTypes = {
  data: PropTypes.array.isRequired,
  width: PropTypes.number.isRequired,
  ratio: PropTypes.number.isRequired,
  type: PropTypes.oneOf(["svg", "hybrid"]).isRequired,
};

CandleStickStockScaleChart.defaultProps = {
  type: "hybrid",
};
CandleStickStockScaleChart = fitWidth(CandleStickStockScaleChart);

export default CandleStickStockScaleChart;
