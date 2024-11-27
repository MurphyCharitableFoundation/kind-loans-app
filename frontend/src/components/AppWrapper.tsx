import { Container } from "@mui/material";
import BottomNavBar from "./BottomNavBar";
import Header from "./Header";
import { useSelector } from "react-redux";


export default function AppWrapper({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <Header sectionTitle={title} />
      <Container maxWidth="lg" sx={{ minHeight: "calc(100dvh - 120px)", py: 2, mb: "56px" }}>
        {children}
      </Container>
      <BottomNavBar />
    </>
  );
}
