import * as React from 'react';
import {Box, Button, SvgIcon} from '@mui/material';
import Typography from '@mui/material/Typography';
import SearchDialog from './components/SearchDialog';
import Divider from '@mui/material/Divider';
import { BorrowerCardWithProgress } from './components/BorrowerCard';
import LandPageCarousel from './components/LandingPageCarousel';
import SortFilterPopover from './components/SortFilterPopper';
import  intro from "../../assets/intro.png";
import {useRef, useState} from "react";
import {useQuery} from "@tanstack/react-query";
import LoanProfile from "../../types/LoanProfile";
import {Error} from "@mui/icons-material";
import {
    DistributingFundsIcon,
    FundingIcon,
    PostingIcon,
    RepaymentIcon,
    StayingConnectedIcon
} from "../../assets/icons.tsx";
import Card from "@mui/material/Card";

// should import from data, dont know how to do that currently :(
// testing area-----------------------------------
const LoanPofileTest = [
    {
        imgPath:"../../../public/free-images.avif",
        loanTitle:"Help Tanya build her small fishing business",
        location:"Bukedea, Uganda",
        timeLine:"xx days",
        progressbarPercent:50,
        fundingProgress:"400"
    },
    {
        imgPath:"../../../public/free-images.avif",
        loanTitle:"Help Tanya build her small fishing business",
        location:"Bukedea, Uganda",
        timeLine:"xx days",
        progressbarPercent:50,
        fundingProgress:"400"
    },
]

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
            <LandingHowItWorks />
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

const howItWorks = [
    {
        icon: PostingIcon,
        title: "Step 1: Posting",
        description: "Women entrepreneurs who’ve been carefully vetted and trained in financial literacy by MCF post their funding requests on Kind Loans."
    },
    {
        icon: FundingIcon,
        title: "Step 2: Funding",
        description: "Lenders (like you) browse requests and choose which ones to support - 100% of your loan goes directly to them."
    },
    {
        icon: DistributingFundsIcon,
        title: "Step 3: Distributing Funds",
        description: "Once a request receives enough support, MCF distributes the money and the repayment period begins."
    },
    {
        icon: StayingConnectedIcon,
        title: "Step 4: Staying Connected",
        description: "Every 3 months, you'll receive updates directly from the entrepreneur about how your support is helping their business grow."
    },
    {
        icon: RepaymentIcon,
        title: "Step 5: Repayment",
        description: "At the end of the loan period, you'll get your money back as Kind Loans credit, which you can withdraw or re-use to help another entrepreneur!"
    },

]

function LandingHowItWorks() {

    return (
        <Box mt='1rem' mb='1rem' margin={4}>
            <Typography variant={"h3"}>
                How It <Typography variant={"h3"} component={"span"} sx={{color: "#4F9816"}}>Works</Typography>
            </Typography>
            {howItWorks.map((item, i) => (
                <Card variant={"outlined"} key={i} sx={{height: "288px", gap: "40px", padding: "24px", border: "1", borderRadius:"12px", display: "flex", flexDirection: "column", marginTop: "24px"}} >
                    <Box borderRadius={"12px"} sx={{backgroundColor: "#4C842214", justifyContent: "center", alignContent: "center", alignItems: "center", display: "flex"}} width={"64px"} height={"64px"}>
                        <item.icon key={i} color={"#4C8422"} />
                    </Box>
                    <Box sx={{marginTop: "auto"}}>
                        <Typography variant={"h3"}>{item.title}</Typography>
                        <Typography variant={"body1"} paddingTop={"16px"}>{item.description}</Typography>
                    </Box>
                </Card>

            ))}
        </Box>
    );
}

function LandingStories() {
    const { data, error } = useQuery<LoanProfile[]>({
        queryKey: ["story-profile"],
        queryFn: async () => {
            const response = await fetch("http://localhost:8000/api/loan/profile?type=stories");
            if (!response.ok) {
                throw Error(<Error>"Network response was not ok"</Error>);
            }
            console.log(response)
            return response.json();
        },
    });

    if (error) {
        return (<Box>
            {error.message}
        </Box>)
    }

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
                <LandPageCarousel profiles={data}/>
                {/* <BorrowerCard /> */}
            </Box>
        </Box>
    );
}

function LandingLoanList({targetRef}:{targetRef: React.Ref<HTMLDivElement>}) {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    const { data, error } = useQuery<LoanProfile[]>({
        queryKey: ["profile"],
        queryFn: async () => {
            const response = await fetch("http://localhost:8000/api/loan/profile");
            if (!response.ok) {
                throw Error(<Error>"Network response was not ok"</Error>);
            }
            console.log(response)
            return response.json();
        },
    });

    if (error) {
        return (<Box>
            {error.message}
        </Box>)
    }

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
                {data?.map((item) => (
                    <BorrowerCardWithProgress imgPath={item.profile_img}
                                              location={item.country+','+item.city}
                                              deadLine={item.deadline_to_receive_loan}
                                              loanTitle={item.title}
                                              remainingBalance={item.remaining_balance}
                                              targetAmount={item.target_amount}/>
                    ))}
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
