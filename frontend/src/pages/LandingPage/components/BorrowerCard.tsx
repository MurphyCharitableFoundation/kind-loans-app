import { Box } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';


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
    timeLine: string
    progressBarPercent: number
    fundingProgress: string
}

const BorrowerCardWithProgress: React.FC<BorrowStoryDetailCardProp> =  ({imgPath,loanTitle,location,timeLine,progressBarPercent,fundingProgress}) => (
    <Card variant={"outlined"} sx={{borderRadius: 3}}>
        <CardMedia
            component="img"
            image={imgPath}
            alt="Borrower Img"
            sx={{ objectFit: "contain" }}
        />
        <CardContent sx={{ px: 2, pt: 2 }}>
            <Typography variant="body1">
                <strong>{loanTitle}</strong>
            </Typography>
            <Typography variant="body2" marginTop={1}>
                {location}
            </Typography>
            <Typography variant="body2" marginTop={2} marginBottom={1}>
                {timeLine} left
            </Typography>
            <LinearProgress variant="determinate" value={progressBarPercent} />
            <Box display="flex" justifyContent="space-between">
                <Typography variant="caption" align="right" width="100%">
                    ${fundingProgress} more to go
                </Typography>
            </Box>
            <Box>
                <Button variant='contained' size={"small"} sx={{borderRadius: 4, backgroundColor: "#034792", boxShadow: "none"}}>
                    View Loan
                </Button>
            </Box>
        </CardContent>
    </Card>
)

// function BorrowerCardWithProgress({imgPath,cardTitle,location,timeLine,progressBarPercent,fundingProgress}}) {
//     return (
//         <Card>
//             <CardMedia
//                 component="img"
//                 image="../../../public/free-images.avif"
//                 alt="Borrower Img"
//             />
//             <CardContent sx={{ px: 2, pt: 2 }}>
//                 <Typography variant="body2">
//                     Help Tanya build her small fishing business
//                 </Typography>
//                 <Box mb="1rem" mt="1rem" display='flex' justifyContent='space-between' alignItems="center">
//                     <Typography variant="caption" sx={{ flexGrow: 1 }}>
//                         Bukedea, Uganda
//                     </Typography>
//                     <Typography variant="caption">
//                         xx days left
//                     </Typography>
//                 </Box>
//                 <LinearProgress variant="determinate" value={50} />
//                 <Box display="flex" justifyContent="space-between">
//                     <Typography variant="caption" align="right" width="100%">
//                         $400 more to go
//                     </Typography>
//                 </Box>
//                 <Box>
//                     <Button variant='contained' >
//                         View Loan
//                     </Button>
//                 </Box>
//             </CardContent>
//         </Card>
//     )
// }

export default BorrowerCard;

export { BorrowerCardWithProgress };
