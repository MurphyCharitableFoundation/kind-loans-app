import { useQuery } from "@tanstack/react-query";
import { Box } from "@mui/material";
import LoanProfileCard from "../../components/LoanProfileCard";
import LoanProfile from "../../types/LoanProfile";


function LoanRequests() {
  const { data, error, isLoading } = useQuery<LoanProfile[]>({
    queryKey: ["loan-profiles"],
    queryFn: async () => {
      const response = await fetch("api/loanprofile/");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
  });

  return isLoading ? (
    <p>Loading...</p>
  ) : error ? (
    <p>Error: {error.message}</p>
  ) : (
    <Box sx={{ display: "flex", gap: 2, flexDirection: "column" }}>
      {data?.map((loanProfile) => (
        <LoanProfileCard key={loanProfile.id} loanProfile={loanProfile} />
      ))}
    </Box>
  );
}

export default LoanRequests;
