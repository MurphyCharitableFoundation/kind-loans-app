import { Box } from '@mui/material';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';


function LoanDetailPage(
    {LoanPofile:{
        imgPath,
        loanTitle,
        timeLine,
        progressbarPercent,
        fundingProgress,
        fundingGoal,
        loanContributors,
        borrowerName,
        loanProfileSummary,
        loanDescription,
        loanDisbursedDate,
        loanTimeline,
        loanRepayDate
    }}){
    return (
        <Box>
            {/* maybe use carousel here lol */}
            <Box component="img" 
            sx={{
                height: 233,
                width: 350,
                maxHeight: { xs: 233, md: 167 },
                maxWidth: { xs: 350, md: 250 },
              }}
              alt="Loan image"
              src={imgPath}
              />
              <LinearProgress variant="determinate" value={progressbarPercent} />
              <Box display="flex" justifyContent="space-between">
                    <Typography variant="caption" align="right" width="100%">
                        ${fundingProgress} more to go
                    </Typography>
              </Box>
              <Typography variant="h2">
                    {loanTitle}
              </Typography>
              <Box>bussiness types here</Box>
              <Box>
                <Typography variant="caption">
                        {timeLine} left
                </Typography>
              </Box>
              <Box>
                <Typography variant="caption">
                        ${fundingProgress} of ${fundingGoal} Funded
                </Typography>
              </Box>
              <Box>
                <Typography variant="caption">
                        ${loanContributors} lenders contributed
                </Typography>
              </Box>          
              <Box>Selection Buttons here</Box>
              <Box mt="2rem" mb="2rem" textAlign="center">
                <Button variant='contained' sx={{width:"100%"}}>
                    Lend Now 
                </Button>
              </Box>
              <Box mt="1rem" mb="1rem">
                <Typography variant="h3">
                        {borrowerName}'s Story
                </Typography>
                <Typography variant="body2">
                        {loanProfileSummary}
                </Typography>
              </Box>
              <Box mt="2rem" mb="2rem" textAlign="center">
                <Button variant='contained' sx={{width:"100%"}}>
                    Share this Story
                </Button>
              </Box>
              <Box mt="1rem" mb="1rem">
                <Typography variant="h3">
                        About this Loan
                </Typography>
                <Typography variant="body2">
                        {loanDescription}
                </Typography>
              </Box>
              <Box mt="1rem" mb="1rem">
                <Typography variant="h6">
                        When will this loan be disbursed? <Typography variant="body2" sx={{display:"inline"}}>{loanDisbursedDate}</Typography>
                </Typography>
                <Typography variant="h6">
                        How long is this loan? <Typography variant="body2" sx={{display:"inline"}}>{loanTimeline}</Typography>
                </Typography>
                <Typography variant="h6">
                        When will this loan be repaid? <Typography variant="body2" sx={{display:"inline"}}>{loanRepayDate}</Typography>
                </Typography>
              </Box>
        </Box>
    )
}




export default LoanDetailPage