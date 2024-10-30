import * as React from 'react';
import Button from '@mui/material/Button';
import FilterListIcon from '@mui/icons-material/FilterList';
import IconButton from '@mui/material/IconButton';
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import SearchDialog from './components/SearchDialog';
import Divider from '@mui/material/Divider';
import Avatar from '@mui/material/Avatar';
import BorrowerCard, { BorrowerCardWithProgress } from './components/BorrowerCard';
import ToggleButtonGroupForBusinesses from './components/ToggleButtonForBusinesses';
// import LandPageCarousel from './components/landingPageCarousel';
// should import from data, dont know how to do that currently :(
// 
  

function Landingpages(){
    const [open, setOpen] = React.useState(false);
  
    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    const [business, setBusiness] = React.useState(() => []);

    const handleBusiness = (event, newBusiness) => {
      setBusiness(newBusiness);
    };

    const [sortOpen,setSortOpen] = React.useState(false);

    const handleClickSortButton = ()=>{
        setSortOpen(!sortOpen)
    }

    // testing area starts
    const numLoans = 1

    // testing area ends

    return (
        <Box elevation={0}>
            <Box mb='0.5rem'>
                <Typography variant='h1' gutterBottom>
                    Lend as little as $25 to help make a dream come true
                </Typography>
                <Typography variant='body2' gutterBottom>
                    We facilitate 0% interest loans to women entrepreneurs who are <u>left out of traditional banking systems</u> so they cangrow their businesses and provide for their families.
                </Typography>
                <Box textAlign='center'>
                    <Button variant='contained' onClick={handleClickOpen}>
                    Choose a person to support
                    </Button>
                </Box>
                <SearchDialog 
                open={open}
                handleClose={handleClose}
                />
            </Box>
            <Divider />
            <Box mt='1rem' mb='1rem'>
                <Box textAlign='center'>
                    <Typography variant='h3'>
                        Our Vision
                    </Typography>
                </Box>
                <Box mt='1rem' mb='1rem'>
                    <Typography varient='body2'>
                        Inspired by a life changing event, Murphy charitable foundation Uganda is a registered non-governmental, humanitarian organization established in 2018 and it’s operating in Eastern Uganda, whose goal is to support the rights and meet the needs of poor people in their communities.
                    </Typography>
                </Box>
                <Box mt='1rem' mb='1rem'>
                    <Typography varient='body2'>
                        Kind loans App started from an idea to help poor entrepreneur women in Uganda without an interest.---------------------
                        ------------------------------------------------------------------------------------------------------------------------
                    </Typography>
                </Box>
                <Box style={{ justifyContent: "center", display: "flex"}} mt='0.5rem' mb='0.5rem'>
                    <Avatar sx={{ width: 50, height: 50 }} alt='Murphy Icon' src='https://s3-alpha-sig.figma.com/img/df53/4857/8174afe277f743864f6e1f065f8a561e?Expires=1731283200&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=Fh~QeGqL9OnCbaj-ecaCWoLIAIOCZLooDABJiYoyN3tqZEiptmY3-LPSc8hil1LENMsYZ3WqwV6JywS8JFP4nRV3KqCBrvkW~~jS5kThxWRAce4sQlqPBhNq~xCe5jQGE3JdfCOzJiQOyM9eoMIZ1174X32DB4WFJ4wJDpq2jtSl5l7FwxgG~X178KFaNR0QgxKLXWghOd7aGxQistO7LkQdKWnIUU9VoLnlDUSbCCI4zMwdm8pxyPqto3p3gWef2Ca~ADPOrYrGRqjOr-Jgd1kpxT8alScOu7vtFAz1taQ0UlR4Qcl2qdVy-XEQKFPmX3GkmueFrGj1IIWJUsFXRw__' />
                </Box>
            </Box>
            <Divider />
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
                    <BorrowerCard />
                </Box>
            </Box>
            <Divider />
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
                <Box mt='1rem' mb='1rem'>
                    <Typography variant='caption'>
                        I want to support someone with a loan for
                    </Typography>
                </Box>
                <Box mt='1rem' mb='1rem' elevation={0}>
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
                    <IconButton aria-label="Sort">
                        <FilterListIcon />
                    </IconButton>
                </Box>
                {/* single card and a filter */}
                {/* filter working on progress */}
                <Box>
                    <BorrowerCardWithProgress />
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
        </Box>
    )
}

export default Landingpages