import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { CssBaseline } from "@mui/material";
import LoanRequests from "./pages/LoanRequests/LoanRequests";
import LandingPage from "./pages/LandingPage/LandingPage";
import LoanSearchPage from "./pages/LandingPage/LoanSearchPage";
import LoanDetailPage from "./pages/LandingPage/LoanDetailPage";
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
import AppTheme from "./theme/ThemeProvider";
import { Toaster } from "react-hot-toast";
import { store } from "./store";
import { Provider } from "react-redux";

const queryClient = new QueryClient();

//testing area starts --------------------
const LoanPofileTest={
  imgPath:"../../../public/free-images.avif",
  loanTitle:"Help Tanya build her small fishing business",
  location:"Bukedea, Uganda",
  timeLine:"xx days",
  progressbarPercent:50,
  fundingProgress:"400",
  fundingGoal:"840",
  loanContributors:"10",
  borrowerName:"Tanya",
  loanProfileSummary:"Insert Tanya’s profile summary here ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
  loanDescription: "“ I’m a 32-year old mother of three with a dream to build my own tailoring business so I can support my family.”",
  loanDisbursedDate:"[DD/MM/YYYY]",
  loanTimeline:"12 months",
  loanRepayDate:"at the end of loan period"
}
//testing area ends --------------------

const router = createBrowserRouter([
  //should add a landing page here
  {
    path: "/",
    element: <AppWrapper children={<LoanRequests />} title="Loan requests" />,
  },
  {
    path: "/landing",
    element: <AppWrapper children={<LandingPage />} title="" />,
  },
  {
    path: "/landing/Search",
    element: <AppWrapper children={<LoanSearchPage />} title="" />,
  },
  {
    path: "/landing/loanDetail",
    element: <AppWrapper children={<LoanDetailPage LoanPofile={LoanPofileTest} />} title="" />,
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
