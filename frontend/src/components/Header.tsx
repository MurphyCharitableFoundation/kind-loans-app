import { useState, MouseEvent } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import Container from "@mui/material/Container";
import Avatar from "@mui/material/Avatar";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import AdbIcon from "@mui/icons-material/Adb";
import profilePic from "../assets/dummypic.png";
import SectionTitle from "./SectionTitle";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { setToken } from "../features/auth/authSlice";
import { RootState } from "../store";
import Cookies from "js-cookie";
import toast from "react-hot-toast";

function Header({ sectionTitle }: { sectionTitle: string }) {
  const dispatch = useDispatch();
  const token = useSelector((state: RootState) => state.auth.token);
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

  const handleOpenUserMenu = (event: MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const signOutHandler = () => {
    Cookies.remove("token");
    dispatch(setToken(null));
    toast.success("Signed out successfully");
  }

  return (
    <AppBar position="sticky" elevation={4}>
      <Container maxWidth="lg" sx={{
          p: 0,
          background: "#2E3036"
      }}>
        <Toolbar disableGutters sx={{ px: 2 }}>
          <AdbIcon sx={{ display: { xs: "none", md: "flex" }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              textDecoration: "none",
            }}
          >
            kind loans
          </Typography>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontWeight: 400,
              // letterSpacing: ".3rem",
              color: "inherit",
              textDecoration: "none",
            }}
          >
            Kind Loans
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          {token && (
            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings">
                <IconButton
                  onClick={handleOpenUserMenu}
                  sx={{ p: 0, borderRadius: "50%" }}
                >
                  <Avatar alt="Remy Sharp" src={profilePic} />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: "45px" }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                <MenuItem key="sign_out" onClick={handleCloseUserMenu}>
                  <Typography sx={{ textAlign: "center" }} onClick={signOutHandler}>
                    Sign out
                  </Typography>
                </MenuItem>
                <MenuItem key="profile" onClick={handleCloseUserMenu}>
                  <Typography sx={{ textAlign: "center" }}>Profile</Typography>
                </MenuItem>
              </Menu>
            </Box>
          )}
          {!token && (
              <Link to="/signin">
              <Button variant='outlined' sx={{ ml: 2, borderRadius: 4, color:"#F0F0F7", borderColor: "#F0F0F7", boxShadow: "none", backgroundColor: "inherit", fontSize:10, font: "Work Sans"}}>
                Log In
              </Button>
            </Link>
          )}
        </Toolbar>
        {sectionTitle!=""&&
        <SectionTitle title={sectionTitle} />
        }{/* do not show while there are not title */}
      </Container>
    </AppBar>
  );
}
export default Header;
