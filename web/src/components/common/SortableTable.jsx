import React from "react";
import PropTypes from "prop-types";
import {
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Toolbar,
  Typography,
  Tooltip,
  IconButton,
} from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import OpenInNewIcon from "@material-ui/icons/OpenInNew";
import TradingIcon from "@material-ui/icons/MonetizationOn";
import { Link } from "react-router-dom";

import ColoredText from "../common/ColoredText";
import InteractiveRefresh from "../common/InteractiveRefresh";
import { format } from "../../utils/formatter";

/**
 * Calculates whether a row is less than b row at the orderBy index
 */
function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

/**
 * Returns ascending/descending comparator based on inputs
 */
function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

/**
 * Implements stableSort on array with comparator
 */
function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

/**
 * Renders TableHead with sorting capabilities
 */
const EnhancedTableHead = ({ order, orderBy, onRequestSort, headCells }) => {
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={
              headCell.formatType === "currency" ||
              headCell.formatType === "float" ||
              headCell.formatType === "number" ||
              headCell.formatType === "percentage"
                ? "right"
                : "left"
            }
            padding={headCell.disablePadding ? "none" : "default"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
};

EnhancedTableHead.propTypes = {
  order: PropTypes.oneOf(["asc", "desc"]),
  orderBy: PropTypes.string,
  onRequestSort: PropTypes.func,
  headCells: PropTypes.array,
};

/**
 * Renders The table Toolbar, including title and refresh button.
 */
const EnhancedTableToolbar = ({ title, handleRefresh }) => {
  return (
    <Toolbar>
      <Grid
        container
        direction="row"
        justify="space-between"
        alignItems="center"
      >
        <Grid item>
          <Typography variant="button" id="tableTitle" component="div">
            {title}
          </Typography>
        </Grid>
        {handleRefresh && (
          <Grid item>
            <InteractiveRefresh
              // aria-label="refresh"
              onClick={handleRefresh}
            />
          </Grid>
        )}
      </Grid>
    </Toolbar>
  );
};

EnhancedTableToolbar.propTypes = {
  title: PropTypes.string,
  handleRefresh: PropTypes.func,
};

export const tableTypes = {
  TEXT: "text",
  NUMBER: "number",
  CURRENCY: "currency",
  DATE: "date",
  FLOAT: "float",
  ID: "id",
  PERCENTAGE: "percentage",
};

/**
 * Sortable Table component for showing tabular data
 */
function EnhancedTable({
  data,
  header,
  title,
  handleDelete, // = null,
  buttons, // = true,
  handleRefresh, // = null,
  toolbar, //==true
}) {
  const [order, setOrder] = React.useState("asc");
  const [orderBy, setOrderBy] = React.useState("calories");

  const handleRequestSort = (_event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  return (
    <div style={{ paddingBottom: "20px" }}>
      { toolbar && (<EnhancedTableToolbar title={title} handleRefresh={handleRefresh}/>) }
      <TableContainer>
        <Table
          aria-labelledby="tableTitle"
          size="medium" // "small"
          aria-label="enhanced table"
        >
          <EnhancedTableHead
            order={order}
            orderBy={orderBy}
            onRequestSort={handleRequestSort}
            rowCount={data.length}
            headCells={header}
          />
          <TableBody>
            {stableSort(data, getComparator(order, orderBy)).map(
              (row, index) => {
                const labelId = `enhanced-table-checkbox-${index}`;
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                    {header.map(({ id, formatType, disablePadding, color }) => {
                      let value = "";
                      switch (formatType) {
                        case "date":
                          const dateObject = new Date(row[id]);
                          value = (
                            <Tooltip
                              title={`${dateObject.toLocaleString()}`}
                              aria-label="timestamp"
                            >
                              <Typography>
                                {dateObject.toLocaleDateString()}
                              </Typography>
                            </Tooltip>
                          );
                          break;
                        case "text":
                          value = row[id];
                          break;
                        case "id":
                        case "number":
                          value = Math.floor(row[id]); // integer
                          break;
                        case "float":
                        case "currency":
                        case "percentage":
                          value = format(row[id]); // 2 decimal place
                          break;
                        default:
                          value = row[id];
                      }
                      return (
                        <TableCell
                          component="th"
                          id={labelId}
                          key={`${labelId}${value}`}
                          scope="row"
                          align={
                            formatType === "currency" ||
                            formatType === "float" ||
                            formatType === "number" ||
                            formatType === "percentage"
                              ? "right"
                              : "left"
                          }
                          padding={disablePadding ? "none" : "default"}
                        >
                          {color ? (
                            <ColoredText color={value > 0 ? "green" : "red"}>
                              {value > 0 && "+"}
                              {formatType === "currency" && "$"}
                              {value}
                              {formatType === "percentage" && "%"}
                            </ColoredText>
                          ) : (
                            <>
                              {formatType === "currency" && "$"}
                              {value}
                              {formatType === "percentage" && "%"}
                            </>
                          )}
                        </TableCell>
                      );
                    })}
                    {buttons && (
                      <>
                        <TableCell padding="checkbox">
                          <Tooltip title="Stock Details">
                            <IconButton
                              component={Link}
                              to={`/stock/${row.symbol}`}
                            >
                              <OpenInNewIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                        <TableCell padding="checkbox">
                          <Tooltip title="Trade">
                            <IconButton
                              component={Link}
                              to={`/trade?symbol=${row.symbol}`}
                            >
                              <TradingIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </>
                    )}
                    {handleDelete && (
                      <TableCell padding="checkbox">
                        <Tooltip title="Remove">
                          <IconButton onClick={() => handleDelete(row)}>
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    )}
                  </TableRow>
                );
              }
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

EnhancedTable.propTypes = {
  /** An array of data points */
  data: PropTypes.array,
  /** An array of objects defining parameters of each column's data type and formatting. */
  header: PropTypes.array,
  /** The title of the table */
  title: PropTypes.string,
  /** If defined, shows a button which runs the defined function to delete the row */
  handleDelete: PropTypes.func,
  /** Whether to show Stock Information and Trade pages for stocks (only applicable if the data is about stocks, should be false for other data) */
  buttons: PropTypes.bool,
  /** If defined, shows a button which runs the defined function to refresh the table */
  handleRefresh: PropTypes.func,
};

EnhancedTable.defaultProps = {
  handleDelete: null,
  buttons: true,
  handleRefresh: null,
  toolbar: true
};

export default EnhancedTable;
