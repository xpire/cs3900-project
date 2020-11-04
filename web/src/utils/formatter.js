/**
 * Formatter function which fixes the number of decimal places
 * @param {number} d number to format
 * @param {integer} decimalPlace number of decimal places
 */
export const format = (d, decimalPlace = 2) => {
  return `${Number(d).toFixed(decimalPlace)}`;
};

// export const money = (d, decimalPlace = 2) => {
//   return `$${Number(d).toFixed(decimalPlace)}`;
// };

// export const percentage = (d, decimalPlace = 2) => {
//   return `${Number(d) >= 0 && "+"}${Number(d).toFixed(decimalPlace)}%`;
// };
