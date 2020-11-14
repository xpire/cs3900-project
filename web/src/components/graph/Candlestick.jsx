import React from "react";
import PropTypes from "prop-types";

import { green, red } from "../common/ColoredText";

import { format } from "d3-format";
import { timeFormat } from "d3-time-format";

import { ChartCanvas, Chart } from "react-stockcharts";
import {
  BarSeries,
  BollingerSeries,
  CandlestickSeries,
  LineSeries,
  StochasticSeries,
} from "react-stockcharts/lib/series";
import { XAxis, YAxis } from "react-stockcharts/lib/axes";

import {
  CrossHairCursor,
  EdgeIndicator,
  CurrentCoordinate,
  MouseCoordinateX,
  MouseCoordinateY,
} from "react-stockcharts/lib/coordinates";
import {
  OHLCTooltip,
  MovingAverageTooltip,
  BollingerBandTooltip,
  StochasticTooltip,
  GroupTooltip,
} from "react-stockcharts/lib/tooltip";
import {
  ema,
  stochasticOscillator,
  bollingerBand,
} from "react-stockcharts/lib/indicator";

import { discontinuousTimeScaleProvider } from "react-stockcharts/lib/scale";
import { fitWidth } from "react-stockcharts/lib/helper";

const bbAppearance = {
  stroke: {
    top: "#964B00",
    middle: "#FF6600",
    bottom: "#964B00",
  },
  fill: "#4682B4",
};
const stoAppearance = {
  stroke: Object.assign({}, StochasticSeries.defaultProps.stroke, {
    top: "#37a600",
    middle: "#b8ab00",
    bottom: "#37a600",
  }),
};

class CandleStickStockScaleChart extends React.Component {
  render() {
    const {
      type,
      data: initialData,
      width,
      height = 500,
      margin = { left: 50, right: 50, top: 70, bottom: 30 },
      ratio,
      leftEdge = false,
      rightYAxis = false,
      rightEdge = true,
    } = this.props;

    const gridHeight = height - margin.top - margin.bottom;
    const gridWidth = width - margin.left - margin.right;

    const showGrid = true;
    const yGrid = showGrid
      ? { innerTickSize: -1 * gridWidth, tickStrokeOpacity: 0.2 }
      : {};
    const xGrid = showGrid
      ? { innerTickSize: -1 * gridHeight, tickStrokeOpacity: 0.2 }
      : {};

    const ema20 = ema()
      .id(0)
      .options({ windowSize: 20 })
      .merge((d, c) => {
        d.ema20 = c;
      })
      .accessor((d) => d.ema20);

    const ema50 = ema()
      .id(2)
      .options({ windowSize: 50 })
      .merge((d, c) => {
        d.ema50 = c;
      })
      .accessor((d) => d.ema50);

    const slowSTO = stochasticOscillator()
      .options({ windowSize: 14, kWindowSize: 3 })
      .merge((d, c) => {
        d.slowSTO = c;
      })
      .accessor((d) => d.slowSTO);
    const fastSTO = stochasticOscillator()
      .options({ windowSize: 14, kWindowSize: 1 })
      .merge((d, c) => {
        d.fastSTO = c;
      })
      .accessor((d) => d.fastSTO);
    const fullSTO = stochasticOscillator()
      .options({ windowSize: 14, kWindowSize: 3, dWindowSize: 4 })
      .merge((d, c) => {
        d.fullSTO = c;
      })
      .accessor((d) => d.fullSTO);

    const bb = bollingerBand()
      .merge((d, c) => {
        d.bb = c;
      })
      .accessor((d) => d.bb);

    const calculatedData = bb(
      ema20(ema50(slowSTO(fastSTO(fullSTO(initialData)))))
    );

    const xScaleProvider = discontinuousTimeScaleProvider.inputDateAccessor(
      (d) => d.date
    );
    const { data, xScale, xAccessor, displayXAccessor } = xScaleProvider(
      calculatedData
    );
    const xExtents = [
      xAccessor(data[data.length - 1]),
      xAccessor(data[data.length > 120 ? data.length - 120 : 0]),
    ];

    return (
      <ChartCanvas
        height={height}
        ratio={ratio}
        width={width}
        margin={margin}
        type={type}
        data={data}
        xScale={xScale}
        xAccessor={xAccessor}
        displayXAccessor={displayXAccessor}
        xExtents={xExtents}
        seriesName="Graph"
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
          <OHLCTooltip
            fontFamily="Roboto"
            fontSize={16}
            textFill="#FFFFFF"
            labelFill="#2196f3"
            origin={[-50, -10]}
          />

          <LineSeries yAccessor={ema20.accessor()} stroke={ema20.stroke()} />
          <LineSeries yAccessor={ema50.accessor()} stroke={ema50.stroke()} />

          <BollingerSeries yAccessor={(d) => d.bb} {...bbAppearance} />
          <BollingerBandTooltip
            origin={[-50, 60]}
            yAccessor={(d) => d.bb}
            options={bb.options()}
            fontFamily="Roboto"
            fontSize={16}
            textFill="#FFFFFF"
            labelFill="#2196f3"
          />

          <CurrentCoordinate
            yAccessor={ema20.accessor()}
            fill={ema20.stroke()}
          />
          <CurrentCoordinate
            yAccessor={ema50.accessor()}
            fill={ema50.stroke()}
          />

          <GroupTooltip
            layout="vertical"
            origin={[-50, 15]}
            verticalSize={20}
            fontFamily="Roboto"
            fontSize={16}
            textFill="#FFFFFF"
            labelFill="#2196f3"
            onClick={(e) => console.log(e)}
            options={[
              {
                yAccessor: ema20.accessor(),
                yLabel: `${ema20.type()}(${ema20.options().windowSize})`,
                valueFill: ema20.stroke(),
                withShape: true,
              },
              {
                yAccessor: ema50.accessor(),
                yLabel: `${ema50.type()}(${ema50.options().windowSize})`,
                valueFill: ema50.stroke(),
                withShape: true,
              },
            ]}
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
              fill={(d) => (d.close > d.open ? green.light : red.dark)} //"#6BA583" : "#DB0000")}
            />
          )}
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
