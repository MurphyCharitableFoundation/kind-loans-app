import * as React from 'react';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import { BorrowerCardWithProgress } from './components/BorrowerCard';
import ToggleButtonGroupForBusinesses from './components/ToggleButtonForBusinesses';
import SortFilterPopover from './components/SortFilterPopper';


// should import from data, dont know how to do that currently :(
// testing area-----------------------------------
const BorrowerCardPofileForTest = {
    imgPath:"../../../public/free-images.avif",
    loanTitle:"Help Tanya build her small fishing business",
    location:"Bukedea, Uganda",
    timeLine:"xx days left",
    progressbarPercent:50,
    fundingProgress:"400"
}

//testing area ends-----------------------------------
  

function LoanSearchPage(){
    const [business, setBusiness] = React.useState(() => []);

    const handleBusiness = (event, newBusiness) => {
      setBusiness(newBusiness);
    };

    // testing area starts---------------
    const numLoans = 1

    // testing area ends-----------------

    return (
        <Box mt='1rem' mb='1rem'>
            <Box mt='1rem' mb='1rem'>
                <Typography variant='h3'>
                    Loan Search
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <Typography variant='caption'>
                    I want to support someone with a loan for
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <ToggleButtonGroupForBusinesses 
                FilterButtonBusinesses={[{id:1,text:"Any business type"} , {id:2,text:"Medical"} , {id:3,text:"Colthing"} ,{id:4,text:"Grocery"}, {id:5,text:"Emergency"},{id:6,text:"Education"},{id:7,text:"Others"}]}
                business={business}
                handleBusiness={handleBusiness}
                />
            </Box>
            <Box mb='0.5rem' display='flex' justifyContent='space-between' alignItems="center">
                <Box textAlign="center" sx={{ flexGrow: 1}}> 
                    <Typography variant='subtitle1'>
                        Total {numLoans} borrowers
                    </Typography>
                </Box>
                <SortFilterPopover />
            </Box>
            <Box>
                <BorrowerCardWithProgress LoanPofile={BorrowerCardPofileForTest}/>
            </Box>
            <Box textAlign="center" mt="2rem" mb="7rem">
                <Button variant="outlined">
                    + View More
                </Button>
            </Box>
            <Box textAlign="center" mb="2rem">
                <Typography variant='subtitle2'>
                    * 100% of your loan goes to supporting borrowers. 
                    <Typography variant="caption">
                        Terms of conditions
                    </Typography>    
                </Typography>
            </Box>
        </Box>
    )
}

export default LoanSearchPage