import Paper from "@mui/material/Paper";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import CreditScoreIcon from "@mui/icons-material/CreditScore";
import ListAltIcon from "@mui/icons-material/ListAlt";
import { Link, useLocation } from "react-router-dom";

export default function BottomNavBar() {
  const location = useLocation();

  return (
    <Paper
      sx={{ position: "fixed", bottom: 0, left: 0, right: 0 }}
      elevation={4}
    >
      <BottomNavigation showLabels value={location.pathname}>
        <BottomNavigationAction
          label="Loan requests"
          icon={<ListAltIcon />}
          component={Link}
          to="/"
          value="/"
        />
        <BottomNavigationAction
          label="My loan request"
          icon={<CreditScoreIcon />}
          component={Link}
          to="/myloanrequest"
          value="/myloanrequest"
        />
      </BottomNavigation>
    </Paper>
  );
}
