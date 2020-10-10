import React from "react";
import {
  Breadcrumbs,
  Link as MaterialLink,
  Typography,
} from "@material-ui/core";
import { Link } from "react-router-dom";

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
