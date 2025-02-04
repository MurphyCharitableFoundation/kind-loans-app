import { Container } from "@mui/material";
import BottomNavBar from "./BottomNavBar";
import Header from "./Header";

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
      <Container maxWidth={false} sx={{
          minHeight: "calc(100dvh - 120px)",
          py: 2,
          mb: "56px",
          margin: 0,
          padding: 0,
      }}>
        {children}
      </Container>
      {
      token && <BottomNavBar /> 
      }
    </>
  );
}
