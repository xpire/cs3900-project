import React from "react";
import PropTypes from "prop-types";
import {
  Breadcrumbs,
  Link as MaterialLink,
  Typography,
} from "@material-ui/core";
import { Link } from "react-router-dom";

/**
 * Component that renders a material-ui breadcrumb
 */
const MyBreadcrumbs = ({ items }) => {
  return (
    <Breadcrumbs>
      {items.map(({ path, name }, i) => {
        return (
          <>
            {i < items.length - 1 ? (
              <MaterialLink component={Link} to={path}>
                {name}
              </MaterialLink>
            ) : (
              <Typography>{name}</Typography>
            )}
          </>
        );
      })}
    </Breadcrumbs>
  );
};

export default MyBreadcrumbs;
