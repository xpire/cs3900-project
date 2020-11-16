import React from "react";
import { motion } from "framer-motion";
import { IconButton, Tooltip } from "@material-ui/core";
import RefreshIcon from "@material-ui/icons/Refresh";

/**
 * An interactive refresh icon button which rotates when clicked
 */
const InteractiveRefresh = ({ onClick }) => {
  return (
    // <Tooltip title="Refresh">
    // <IconButton onClick={onClick}>
    //   <motion.div
    //     // whileTap={{ rotate: 180 }}
    //     style={{ height: "24px" }}
    //   >
    <RefreshIcon {...onClick} />
    //     </motion.div>
    //   </IconButton>
    // </Tooltip>
  );
};

export default InteractiveRefresh;
