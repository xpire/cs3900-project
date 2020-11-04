import React, { useEffect, Fragment } from "react";
import { withRouter } from "react-router-dom";

/**
 * A React component that provides fluid page transitions by scrolling to the top of a new page when react router changes pages
 */
function ScrollToTop({ history, children }) {
  useEffect(() => {
    const unlisten = history.listen(() => {
      window.scrollTo(0, 0);
    });
    return () => {
      unlisten();
    };
  }, [history]);

  return <Fragment>{children}</Fragment>;
}

export default withRouter(ScrollToTop);
