import { Container } from "@mui/material";
import BottomNavBar from "./BottomNavBar";
import Header from "./Header";
import { useSelector } from "react-redux"
import { RootState } from "../store";

export default function AppWrapper({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  // const token = useSelector((state:RootState) => state.auth.token);
  const token = true;
  return (
    <>
      <Header sectionTitle={title} />
      <Container maxWidth="lg" sx={{ minHeight: "calc(100dvh - 120px)", py: 2, mb: "56px" }}>
        {children}
      </Container>
      {
      token && <BottomNavBar /> 
      }
    </>
  );
}
