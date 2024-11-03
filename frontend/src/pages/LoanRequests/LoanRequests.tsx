import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Box } from "@mui/material";
import LoanProfileCard from "../../components/LoanProfileCard";
import LoanProfile from "../../types/LoanProfile";
import UploadWidget from "../../components/UploadWidget";
import { AdvancedImage, responsive, placeholder } from "@cloudinary/react";
import { useSelector } from "react-redux";
import { RootState } from "../../store";

function LoanRequests() {
  const myCld = useSelector((state: RootState) => state.cloudinary.myCld);
  const [imageId, setImageId] = useState<string>("");

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
      <h3>Cloudinary Upload Widget Example</h3>
      <UploadWidget setImageId={setImageId} />
      {imageId && (
        <div style={{ width: "800px" }}>
          <AdvancedImage
            style={{ maxWidth: "100%" }}
            cldImg={myCld.image(imageId)}
            plugins={[responsive(), placeholder()]}
          />
        </div>
      )}
    </Box>
  );
}

export default LoanRequests;
