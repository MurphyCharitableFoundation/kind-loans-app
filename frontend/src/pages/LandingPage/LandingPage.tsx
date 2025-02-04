import * as React from 'react';
import {Box, Button} from '@mui/material';
import Typography from '@mui/material/Typography';
import SearchDialog from './components/SearchDialog';
import Divider from '@mui/material/Divider';
import Avatar from '@mui/material/Avatar';
import { BorrowerCardWithProgress } from './components/BorrowerCard';
import ToggleButtonGroupForBusinesses from './components/ToggleButtonForBusinesses';
import LandPageCarousel from './components/LandingPageCarousel';
import SortFilterPopover from './components/SortFilterPopper';
import  intro from "../../assets/intro.png";

// should import from data, dont know how to do that currently :(
// testing area-----------------------------------
const LoanPofileTest = {
    imgPath:"../../../public/free-images.avif",
    loanTitle:"Help Tanya build her small fishing business",
    location:"Bukedea, Uganda",
    timeLine:"xx days",
    progressbarPercent:50,
    fundingProgress:"400"
}

//testing area ends-----------------------------------

function Landingpage(){

    // testing area ends-----------------

    return (
        <Box>
            <LandingIntro />
            <Divider />
            <LandingVision />
            <Divider />
            <LandingStories />
            <Divider />
            <LandingLoanList />
        </Box>
    )
}

function LandingIntro() {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Box mb='0.5rem' margin={0} alignItems={'end'} display={"flex"} sx={{
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${intro})`,
            height: "568px",
            color: "white",
        }}>
            <Box margin={4}>
                <Typography variant='h4' gutterBottom={true}>
                    Lend as little as $25 to help make a dream come true
                </Typography>
                <Typography variant='h6' gutterBottom={true}>
                    100% of your loan goes to supporting entrepreneurs in need.
                </Typography>
                <Box textAlign='center'>
                    <Button variant='contained' sx={{
                        background: "#034792",
                        borderRadius: 4,
                    }} fullWidth={true} onClick={handleClickOpen}>
                        Browse loans
                    </Button>
                </Box>
                <SearchDialog
                    open={open}
                    handleClose={handleClose}
                />
            </Box>
        </Box>
    );
}

function LandingVision() {
    return (
        <Box mt='1rem' mb='1rem' margin={4}>
            <Box textAlign='center'>
                <Typography variant='h4'>
                    Our <Typography variant='h4' component={"span"} sx={{color: "#4F9816"}}>Vision</Typography>
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <Typography variant='body1'>
                    The Kind Loans App was created by the <Typography component="span" variant='body1' ss={{textDecoration: "underline"}}>Murphy Charitable Foundation (MCF)</Typography> to meet the needs of poor women entrepreneurs in Uganda who lack access to traditional banks.
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <Typography variant='body1'>
                    This app enables lenders to easily fund <strong>interest-free</strong> micro-loans for women entrepreneurs in Uganda, enabling them to start and grow their small businesses, pursue education, and improve the quality of life for their families.
                </Typography>
            </Box>
            <Box style={{ justifyContent: "center", display: "flex"}} mt='0.5rem' mb='0.5rem'>
                <Avatar sx={{ width: 50, height: 50 }} alt='Murphy Icon' src='https://s3-alpha-sig.figma.com/img/df53/4857/8174afe277f743864f6e1f065f8a561e?Expires=1731283200&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=Fh~QeGqL9OnCbaj-ecaCWoLIAIOCZLooDABJiYoyN3tqZEiptmY3-LPSc8hil1LENMsYZ3WqwV6JywS8JFP4nRV3KqCBrvkW~~jS5kThxWRAce4sQlqPBhNq~xCe5jQGE3JdfCOzJiQOyM9eoMIZ1174X32DB4WFJ4wJDpq2jtSl5l7FwxgG~X178KFaNR0QgxKLXWghOd7aGxQistO7LkQdKWnIUU9VoLnlDUSbCCI4zMwdm8pxyPqto3p3gWef2Ca~ADPOrYrGRqjOr-Jgd1kpxT8alScOu7vtFAz1taQ0UlR4Qcl2qdVy-XEQKFPmX3GkmueFrGj1IIWJUsFXRw__' />
            </Box>
        </Box>
    );
}

function LandingStories() {
    return (
        <Box mt='1rem' mb='1rem'>
            <Box textAlign='center' mt='1rem' mb='1rem'>
                <Typography variant='h3'>
                    Borrower Stories
                </Typography>
            </Box>
            <Box textAlign='center' mt='1rem' mb='1rem'>
                <Typography varient='subtitle2'>
                    Hear from our borrowers
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                {/* just leave a singe card here for now */}
                <LandPageCarousel />
                {/* <BorrowerCard /> */}
            </Box>
        </Box>
    );
}

function LandingLoanList() {
    const [business, setBusiness] = React.useState(() => []);

    const handleBusiness = (event, newBusiness) => {
        setBusiness(newBusiness);
    };

    // testing area starts---------------
    const numLoans = 1

    return (
        <Box mt='1rem' mb='1rem'>
            <Box textAlign='center' mt='1rem' mb='1rem'>
                <Typography variant='h3'>
                    Almost there!
                </Typography>
            </Box>
            <Box textAlign='center' mt='1rem' mb='1rem'>
                <Typography variant='subtitle1'>
                    Lend the last few dollars they need
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem' textAlign="center">
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
            {/* single card and a filter */}
            {/* filter working on progress */}
            <Box>
                <BorrowerCardWithProgress LoanPofile={LoanPofileTest}/>
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

    );
}

export default Landingpage