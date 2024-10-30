import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { CssBaseline } from "@mui/material";
import LoanRequests from "./pages/LoanRequests/LoanRequests";
import MyLoanRequest from "./pages/MyLoanRequest/MyLoanRequest";
import NotFound from "./pages/NotFound/NotFound";
import "./index.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import AppWrapper from "./components/AppWrapper";
import SignIn from "./pages/SignIn/SignIn";
import SignUp from "./pages/SignUp/SignUp";
import Profile from "./pages/Profile/Profile";
import AppTheme from "./theme/ThemeProvider";
import { Toaster } from "react-hot-toast";
import { store } from "./store";
import { Provider } from "react-redux";

const queryClient = new QueryClient();

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppWrapper children={<LoanRequests />} title="Loan requests" />,
  },
  {
    path: "/myloanrequest",
    element: (
      <AppWrapper children={<MyLoanRequest />} title="My loan request" />
    ),
  },
  {
    path: "/signin",
    element: <AppWrapper children={<SignIn />} title="Sign in" />,
  },
  {
    path: "/signup",
    element: <AppWrapper children={<SignUp />} title="Sign up" />,
  },
  {
    path: "/profile",
    element: <AppWrapper children={<Profile />} title="Sign up" />,
  },
  {
    path: "*",
    element: <AppWrapper children={<NotFound />} title="Not found" />,
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AppTheme>
        <CssBaseline />
        <Toaster position="bottom-center" />
        <Provider store={store}>
          <RouterProvider router={router} />
        </Provider>
      </AppTheme>
    </QueryClientProvider>
  </StrictMode>
);
