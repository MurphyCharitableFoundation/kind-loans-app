import { Box } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import React from "react";


interface BorrowStoryCardProp {
    imgPath: string;
    loanDescription: string;
    location:string;
}

const BorrowerCard: React.FC<BorrowStoryCardProp> = ({imgPath, loanDescription, location}) => (
    <Card>
        <Box height={239}>
            <CardMedia
                component="img"
                image={imgPath}
                alt="Borrower Img"
                sx={{ objectFit: "contain", borderRadius: 4}}
            />
        </Box>
        <CardContent sx={{padding: 0}}>
            <Typography variant={"body2"}>
                {loanDescription}
            </Typography>
            <Typography variant={"caption"} paddingTop={2}>
                {location}
            </Typography>
        </CardContent>
    </Card>
)

interface BorrowStoryDetailCardProp {
    imgPath: string
    loanTitle: string
    location: string
    deadLine: string
    targetAmount: string
    remainingBalance: string
}

const BorrowerCardWithProgress : React.FC<BorrowStoryDetailCardProp> = (profile) => {
    const remainingAmount = Number(profile.targetAmount) - Number(profile.remainingBalance)
    const progressBar = remainingAmount/Number(profile.targetAmount)

    return (
    <Card variant={"outlined"} sx={{borderRadius: 3}}>
        <CardMedia
            component="img"
            image={profile.imgPath}
            alt="Borrower Img"
            sx={{objectFit: "contain"}}
        />
        <CardContent sx={{px: 2, pt: 2}}>
            <Typography variant="body1">
                <strong>{profile.loanTitle}</strong>
            </Typography>
            <Typography variant="body2" marginTop={1}>
                {profile.location}
            </Typography>
            <Typography variant="body2" marginTop={2} marginBottom={1}>
                {getDaysBetween(new Date(profile.deadLine))} days left
            </Typography>
            <LinearProgress variant="determinate" value={progressBar}/>
            <Box display="flex" justifyContent="space-between">
                <Typography variant="caption" align="right" width="100%">
                    ${remainingAmount} more to go
                </Typography>
            </Box>
            <Box>
                <Button variant='contained' size={"small"}
                        sx={{borderRadius: 4, backgroundColor: "#034792", boxShadow: "none"}}>
                    View Loan
                </Button>
            </Box>
        </CardContent>
    </Card>
    );
}
function getDaysBetween(date: Date): number {
    const now = new Date();
    const timeDiff = Math.abs(now.getTime() - date.getTime());
    return Math.floor(timeDiff / (1000 * 60 * 60 * 24)); // Convert milliseconds to days
}

export default BorrowerCard;

export { BorrowerCardWithProgress };
