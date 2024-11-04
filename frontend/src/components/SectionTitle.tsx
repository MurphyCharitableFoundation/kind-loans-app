import { Paper, Typography } from "@mui/material";

export default function SectionTitle({ title }: { title: string }) {
  return (
    <Paper
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        py: 1,
        bgcolor: "background.default",
        borderTop: 1,
        borderBottom: 1,
        borderColor: "divider",
        borderRadius: 0,
      }}
      elevation={4}
    >
      <Typography variant="h6" component="h6" sx={{ px: 2 }}>
        {title}
      </Typography>
    </Paper>
  );
}
