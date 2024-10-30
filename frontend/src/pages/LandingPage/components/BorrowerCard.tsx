import { Box } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

// should have two types maybe but just image + story and image + progress bar?
const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
    height: 10,
    borderRadius: 5,
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
  }));

function BorrowerCard (props){
    return (
        <Card>
            <CardMedia
            component="img"
            height="40%"
            image="../../../public/free-images.avif"
            alt="Borrower Img"
            sx={{mb:"1rem",mt:"1rem"}}
            />
            <CardContent>
                <Typography variant="body2" sx={{mb:"1rem",mt:"1rem"}}>
                    "I'm a 32-year old mother of three with a dream to build my own tailoring business so I can support my family."
                </Typography>
                <Typography variant="caption" sx={{mb:"1rem",mt:"1rem"}}>
                    -Monal, Clothing shop owner in Uganda
                </Typography>
            </CardContent>
      </Card>
    )
}

function BorrowerCardWithProgress (props){
    return (
        <Card>
            <CardMedia
            component="img"
            height="40%"
            image="../../../public/free-images.avif"
            alt="Borrower Img"
            sx={{mb:"1rem",mt:"1rem"}}
            />
            <CardContent>
                <Typography variant="body2" sx={{mb:"1rem",mt:"1rem"}}>
                    Help Tanya build her small fishing business
                </Typography>
                <Box mb="1rem" mt="1rem" display='flex' justifyContent='space-between' alignItems="center">
                    <Typography variant="caption" sx={{flexGrow: 1}}>
                        Bukedea, Uganda
                    </Typography>
                    <Typography variant="caption">
                        xx days left
                    </Typography>
                </Box>
                <BorderLinearProgress variant="determinate" value={50} />
                <Box display="flex" justifyContent="space-between">
                    <Typography variant="caption" align="right" width="100%">
                        $400 more to go
                    </Typography>
                </Box>
                <Button variant='contained'>
                    View Loan
                </Button>
            </CardContent>
        </Card>
    )
}

export default BorrowerCard;

export {BorrowerCardWithProgress};