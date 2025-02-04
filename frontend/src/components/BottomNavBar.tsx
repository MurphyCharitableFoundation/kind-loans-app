import Paper from "@mui/material/Paper";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import SearchIcon from '@mui/icons-material/Search';
import DashboardIcon from '@mui/icons-material/Dashboard';
import { Link, useLocation } from "react-router-dom";


export default function BottomNavBar() {
  const location = useLocation();
  //if logged in then show this else nothing but a grey bar?
  return (
    <Paper
      sx={{ position: "fixed", bottom: 0, left: 0, right: 0 }}
      elevation={4}
    >
      <BottomNavigation showLabels value={location.pathname}>
        <BottomNavigationAction
          label="Search"
          icon={<SearchIcon />}
          component={Link}
          to="/"
          value="/"
        />
        <BottomNavigationAction
          label="My Dashboard"
          icon={<DashboardIcon />}
          component={Link}
          to="/myloanrequest"
          value="/myloanrequest"
        />
      </BottomNavigation>
    </Paper>
  );
  //nothing shown if not loggin, refer to token/auth
}
