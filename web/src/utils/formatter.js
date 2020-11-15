/**
 * Formatter function which fixes the number of decimal places
 * @param {number} d number to format
 * @param {integer} decimalPlace number of decimal places
 */
export const format = (d, decimalPlace = 2) => {
  return new Number(d).toFixed(decimalPlace);
};

export const formatToCurrency = (d) => {
  if (d < 0) {
    return `-$${(-d).toFixed(2)}`;
  }
  return `$${d.toFixed(2)}`;
};

export const formatWithPlus = (d) => {
  return (d < 0 ? "" : "+") + d.toFixed(2);
};
