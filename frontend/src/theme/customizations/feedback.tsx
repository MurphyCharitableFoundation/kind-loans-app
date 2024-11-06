import { Theme, alpha, Components } from "@mui/material/styles";
import { gray, orange } from "./themePrimitives";
import { linearProgressClasses } from '@mui/material/LinearProgress';

export const feedbackCustomizations: Components<Theme> = {
  MuiAlert: {
    styleOverrides: {
      root: ({ theme }) => ({
        borderRadius: 10,
        backgroundColor: orange[100],
        color: theme.palette.text.primary,
        border: `1px solid ${alpha(orange[300], 0.5)}`,
        "& .MuiAlert-icon": {
          color: orange[500],
        },
      }),
    },
  },
  MuiDialog: {
    styleOverrides: {
      root: ({ theme }) => ({
        "& .MuiDialog-paper": {
          borderRadius: "10px",
          border: "1px solid",
          borderColor: theme.palette.divider,
        },
      }),
    },
  },
  MuiLinearProgress: {
    styleOverrides: {
      root: ({theme}) => ({
        height: 10,
        borderRadius: 5,
        backgroundColor: gray[200],
        [`&.${linearProgressClasses.colorPrimary}`]: {
          backgroundColor: theme.palette.grey[200],
          ...theme.applyStyles('dark', {
            backgroundColor: theme.palette.grey[800],
          }),
        },
        [`& .${linearProgressClasses.bar}`]: {
          borderRadius: 5,
          backgroundColor: '#1a90ff',
          ...theme.applyStyles('dark', {
            backgroundColor: '#308fe8',
          }),
        },
      }),
    },
  },
};
