const md = `**Those curves giving you trouble?**

There are multitudes of graphs and charts that traders use to make informed decisions about their investments. We've given you a few of the popular ones, subject to your level.

---

***Candlestick Graph***
This is the bread and butter chart for traders. Each data point represents the stocks key movements throughout a day, and contains a coloured vertical line and rectangular box. Here's how to interpret those:
* Colour: Green means the stock went up in price that day, Red means it went down
* Vertical Line: the top of the line is the highest price that stock reached during that day, and the bottom of the line is the lowest price.
* Rectangular Box: the top and bottom edges of the box represent the opening and closing price of that stock for the day. If the data point is red, the top is opening price and bottom is closing price. Flip these if the point is green. 

---

***Volume Graph***
This graph represents the total number of shares that _moved_ each day - the sum of the volumes bought and sold. It's essentially a measure of how popular a stock is to trade, giving some indication to that stocks future performance and volatility.

E.g. rising stocks with high volumes generally means there are more buyers than sellers, increasing demand which then increases price.

---

***Exponential Moving Average (EMA) Graph***
EMA is a slightly more complex graph to interpret. It calculates the average stock price within a certain time period (in our case, 20 days), and gives increasing weight to more recent data points.

It's generally used to indicate when a stock has diverged from the historical average, and thus may be a good time to buy or sell.

---

***Bollinger Bands (BB)***
Ok, this is a pretty complex chart that we've provided simply because it looks cool.

Essentially, it creates an "envolope" that consists of 3 key features: an upper band, a lower band, and a standard moving average (SMA). The upper and lower bands are 2 standard deviations above and below the SMA, and so the width of the envolope can represent the volatility of the stock.

These bands should also contain roughly 90% of the stocks price movements, so any movement outside these bands can be considered "relatively" high or low, similar to the EMA.`;

export default md