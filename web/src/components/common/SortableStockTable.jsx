import React, { useEffect, useState, forwardRef } from "react";
import MaterialTable from "material-table";
import { Grid, Typography, Tooltip } from "@material-ui/core";
import PropTypes from "prop-types";
import { useHistory } from "react-router-dom";

import ColoredText from "./ColoredText";
import { format, formatToCurrency } from "../../utils/formatter";
import InteractiveRefresh from "../common/InteractiveRefresh";

import OpenInNewIcon from "@material-ui/icons/OpenInNew";
import DeleteIcon from "@material-ui/icons/Delete";

import AddBox from "@material-ui/icons/AddBox";
import ArrowDownward from "@material-ui/icons/ArrowDownward";
import Check from "@material-ui/icons/Check";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Clear from "@material-ui/icons/Clear";
import DeleteOutline from "@material-ui/icons/DeleteOutline";
import Edit from "@material-ui/icons/Edit";
import FilterList from "@material-ui/icons/FilterList";
import FirstPage from "@material-ui/icons/FirstPage";
import LastPage from "@material-ui/icons/LastPage";
import Remove from "@material-ui/icons/Remove";
import SaveAlt from "@material-ui/icons/SaveAlt";
import Search from "@material-ui/icons/Search";
import ViewColumn from "@material-ui/icons/ViewColumn";

export const tableTypes = {
  TEXT: "text",
  NUMBER: "number",
  CURRENCY: "currency",
  DATE: "date",
  FLOAT: "float",
  ID: "id",
  PERCENTAGE: "percentage",
  SHARES: "shares",
};

const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => (
    <ChevronRight {...props} ref={ref} />
  )),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => (
    <ChevronLeft {...props} ref={ref} />
  )),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
};

export const ConditionalColorText = ({
  initialValue,
  formatType,
  color = false,
  secondary = false,
  negative = false,
  ...otherProps
}) => {
  let value = "";
  switch (formatType) {
    case "date":
      const dateObject = new Date(initialValue);
      value = (
        <Tooltip
          title={`${dateObject.toLocaleString()}`}
          aria-label="timestamp"
        >
          <Typography variant={`h6`}>
            {dateObject.toLocaleDateString()}
          </Typography>
        </Tooltip>
      );
      break;
    case "text":
      value = initialValue;
      break;
    case "id":
    case "number":
      value = Math.floor(initialValue); // integer
      break;
    case "shares":
      value = `${Math.floor(initialValue)} Shares`;
      break;
    case "percentage":
      value = format(100 * initialValue); // 2 decimal place
    case "float":
    case "currency":
      value = format(initialValue);
      break;
    default:
      value = initialValue;
  }
  return (
    <>
      {color ? (
        <ColoredText
          {...otherProps}
          color={
            (value > 0 && !negative) || (value <= 0 && !!negative)
              ? "green"
              : "red"
          }
        >
          {value > 0 && "+"}
          {/* {formatType === "currency" && "$"} */}
          {value}
          {formatType === "percentage" && "%"}
        </ColoredText>
      ) : (
        <Typography
          {...otherProps}
          color={secondary ? "textSecondary" : "textPrimary"}
        >
          {formatType === "currency" ? (
            <>
              {(value < 0 ? "-" : "") + "$"}
              {Math.abs(value)}
            </>
          ) : (
            <>
              {value}
              {formatType === "percentage" && "%"}
            </>
          )}
        </Typography>
      )}
    </>
  );
};

export const RenderItem = ({
  title,
  titleType = tableTypes.TEXT,
  titleColor = false,

  subtitle = undefined,
  subtitleType = tableTypes.TEXT,
  subtitleColor = false,
  subtitleNegative = false,

  subsubtitle = undefined,
  subsubtitleType = tableTypes.TEXT,
  subsubtitleColor = false,
  subsubtitleNegative = false,

  alignItems = "flex-end",
}) => {
  return (
    <Grid container direction="column" alignItems={alignItems}>
      <Grid item>
        <ConditionalColorText
          initialValue={title}
          formatType={titleType}
          color={titleColor}
          align={alignItems === "flex-end" ? "right" : "left"}
          variant={`h6`}
        />
      </Grid>
      <Grid item container spacing={1} direction="row" justify={alignItems}>
        {subtitle !== undefined && (
          <Grid item>
            <ConditionalColorText
              initialValue={subtitle}
              formatType={subtitleType}
              color={subtitleColor}
              align={alignItems === "flex-end" ? "right" : "left"}
              secondary={true}
              negative={subtitleNegative}
              variant={`button`}
            />
          </Grid>
        )}
        {subtitle !== undefined && (
          <Grid item>
            <ConditionalColorText
              initialValue={subsubtitle}
              formatType={subsubtitleType}
              color={subsubtitleColor}
              align={alignItems === "flex-end" ? "right" : "left"}
              secondary={true}
              negative={subsubtitleNegative}
              variant={`button`}
            />
          </Grid>
        )}
      </Grid>
    </Grid>
  );
};

const SortableStockTable = ({
  title,
  columns,
  data,
  isLoading,
  handleDelete, // = null,
  buttons, // = true,
  handleRefresh, // = null,
}) => {
  let history = useHistory();
  const [actions, setActions] = useState([]);
  useEffect(() => {
    let actionsConst = [];

    !!buttons &&
      actionsConst.push({
        icon: OpenInNewIcon,
        tooltip: "More Details",
        disabled: !buttons,
        hidden: !buttons,
        onClick: (_event, rowData) => history.push(`/stock/${rowData.symbol}`),
      });
    !!handleDelete &&
      actionsConst.push({
        icon: DeleteIcon,
        tooltip: "Delete",
        disabled: !handleDelete,
        hidden: !handleDelete,
        onClick: (_event, rowData) => handleDelete(rowData),
      });

    !!handleRefresh &&
      actionsConst.push({
        icon: InteractiveRefresh,
        tooltip: "Refresh Table",
        disabled: !handleRefresh,
        hidden: !handleRefresh,
        isFreeAction: true,
        onClick: handleRefresh,
      });
    setActions(actionsConst);
  }, []);
  return (
    <MaterialTable
      title={<Typography variant="button">{title}</Typography>}
      columns={columns.map((c) => ({ ...c, tableData: undefined }))}
      data={data}
      icons={tableIcons}
      isLoading={isLoading}
      options={{
        paging: true,
        search: true,
        actionsColumnIndex: -1,
        draggable: false,
      }}
      localization={{ header: { actions: "" } }}
      actions={actions}
    />
  );
};

SortableStockTable.propTypes = {
  /** An array of data points */
  data: PropTypes.array,
  /** An array of objects defining parameters of each column's data type and formatting. */
  columns: PropTypes.array,
  /** The title of the table */
  title: PropTypes.string,
  /** Whether to show loading spinner or not */
  isLoading: PropTypes.bool,
  /** If defined, shows a button which runs the defined function to delete the row */
  handleDelete: PropTypes.func,
  /** Whether to show Stock Information and Trade pages for stocks (only applicable if the data is about stocks, should be false for other data) */
  buttons: PropTypes.bool,
  /** If defined, shows a button which runs the defined function to refresh the table */
  handleRefresh: PropTypes.func,
};

SortableStockTable.defaultProps = {
  handleDelete: null,
  buttons: true,
  handleRefresh: null,
};

export default SortableStockTable;
