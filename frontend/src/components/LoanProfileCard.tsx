import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import LoanProfile from "../types/LoanProfile";

export default function LoanProfileCard({ loanProfile }: { loanProfile: LoanProfile }) {
  return (
    <Card sx={{ minWidth: 275 }} >
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {loanProfile.title}
        </Typography>
        <Typography variant="body2">
          Help {loanProfile.user_name} with her {loanProfile.business_type} business.
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" sx={{ padding: 0 }}>Learn More</Button>
      </CardActions>
    </Card>
  );
}
