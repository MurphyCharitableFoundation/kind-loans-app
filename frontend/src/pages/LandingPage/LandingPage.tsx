import * as React from 'react';
import {Box, Button} from '@mui/material';
import Typography from '@mui/material/Typography';
import SearchDialog from './components/SearchDialog';
import Divider from '@mui/material/Divider';
import { BorrowerCardWithProgress } from './components/BorrowerCard';
import LandPageCarousel from './components/LandingPageCarousel';
import SortFilterPopover from './components/SortFilterPopper';
import  intro from "../../assets/intro.png";
import {useRef} from "react";

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
    const targetRef = useRef<HTMLDivElement>(null);

    const handleScroll = () => {
        if (targetRef.current) {
            targetRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    };
    // testing area ends-----------------

    return (
        <Box>
            <LandingIntro onAction={handleScroll} />
            <Divider />
            <LandingVision />
            <Divider />
            <LandingStories />
            <Divider />
            <LandingLoanList targetRef={targetRef} />
        </Box>
    )
}

function LandingIntro({onAction}) {
    return (
        <Box mb='0.5rem' margin={0} alignItems={'end'} display={"flex"} sx={{
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${intro})`,
            height: "568px",
            color: "white",
        }}>
            <Box margin={4}>
                <Typography gutterBottom={true} variant={"h2"}>
                    <strong>Lend as little as $25 to help make a dream come true</strong>
                </Typography>
                <Typography gutterBottom={true} variant={"h4"}>
                    100% of your loan goes to supporting entrepreneurs in need.
                </Typography>
                <Box textAlign='center' marginTop={2}>
                    <Button variant='contained' sx={{
                        background: "#034792",
                        borderRadius: 4,
                    }} fullWidth={true} onClick={onAction}>
                        Browse loans
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

function LandingVision() {
    return (
        <Box mt='1rem' mb='1rem' margin={4}>
            <Box>
                <Typography variant={"h3"}>
                    Our <Typography variant={"h3"} component={"span"} sx={{color: "#4F9816"}}>Vision</Typography>
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <Typography variant={"body2"}>
                    The Kind Loans App was created by the <Typography component="span" variant='body1'>Murphy Charitable Foundation (MCF)</Typography> to meet the needs of poor women entrepreneurs in Uganda who lack access to traditional banks.
                </Typography>
            </Box>
            <Box mt='1rem' mb='1rem'>
                <Typography variant={"body2"}>
                    This app enables lenders to easily fund <strong>interest-free</strong> micro-loans for women entrepreneurs in Uganda, enabling them to start and grow their small businesses, pursue education, and improve the quality of life for their families.
                </Typography>
            </Box>
        </Box>
    );
}

function LandingStories() {
    return (
        <Box mt='1rem' mb='1rem'>
            <Box margin={4}>
                <Box mt='1rem' mb='1rem'>
                    <Typography variant={"h3"}>
                        Impact <Typography variant={"h3"} component={"span"} sx={{color: "#4F9816"}}>Stories</Typography>
                    </Typography>
                </Box>
                <Box mt='1rem' mb='1rem'>
                    <Typography variant='subtitle2'>
                        Hear from the entrepreneurs that Kind Loans supports.
                    </Typography>
                </Box>
            </Box>
            <Box mt='1rem' mb='1rem'>
                {/* just leave a singe card here for now */}
                <LandPageCarousel />
                {/* <BorrowerCard /> */}
            </Box>
        </Box>
    );
}

function LandingLoanList({targetRef}) {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Box ref={targetRef} margin={4} mt='1rem' mb='1rem'>
            <Box mt='1rem' mb='1rem'>
                <Typography variant='h3'>
                    <Typography variant='h3' component={"span"} sx={{color: "#4F9816"}}>Find</Typography> a Loan to Support
                </Typography>
            </Box>
            <SearchDialog
                open={open}
                handleClose={handleClose}
            />
            <Box mb='0.5rem' display='flex' justifyContent='space-between' alignItems="center">
                <Box marginTop={2} width={188}>
                    <Button variant='outlined' size='small' sx={{
                        border: "1px solid #74777F",
                        borderRadius: 4,
                        color: "#034792",
                        fontSize: "12px",
                        fontWeight: 500,
                    }} onClick={handleClickOpen}>
                        Filter by Category
                    </Button>
                </Box>
                <SortFilterPopover />
            </Box>
            {/* single card and a filter */}
            {/* filter working on progress */}
            <Box marginTop={2}>
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