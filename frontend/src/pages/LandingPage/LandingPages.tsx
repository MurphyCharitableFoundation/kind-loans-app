import * as React from 'react';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import { Box } from "@mui/material";
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

// should import from data, dont know how to do that currently :(
const FilterButtonBusinesses = [{id:1,text:"Any business type"} , {id:2,text:"Medical"} , {id:3,text:"Colthing"} ,{id:4,text:"Grocery"}, {id:5,text:"Emergency"},{id:6,text:"Education"},{id:7,text:"Others"}]

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
      padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
      padding: theme.spacing(1),
    },
  }));
  

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

    return (
        <Paper elevation={0}>
            <h1>Lend as little as $25 to help make a dream come true</h1>
            <p>We facilitate 0% interest loans to women entrepreneurs who are <u>left out of traditional banking systems</u> so they cangrow their businesses and provide for their families.</p>
            <Box textAlign='center'>
                <Button variant="contained" onClick={handleClickOpen}>
                Choose a person to support
                </Button>
            </Box>
            <BootstrapDialog
            onClose={handleClose}
            aria-labelledby="customized-dialog-title"
            open={open}
            fullWidth={true}
            maxWidth={"sm"}
            >
                <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
                Filter - Loan Search
                </DialogTitle>
                {/* should have some paddings here */}
                <p>I want to support someone with a loan for</p>
                <ToggleButtonGroup value={business} onChange={handleBusiness} sx={{ flexWrap: "wrap"}}>
                    {FilterButtonBusinesses.map((business) => {
                        return <ToggleButton 
                                key={business.id} 
                                value={business.text}
                                sx={{ margin: 2,"&.Mui-selected, &.Mui-selected:hover": {backgroundColor: '#07001C!important'}}}
                                style={{borderRadius: '12px', color:'#FFFFFF',backgroundColor: '#A3A3A3'}}
                                >
                            {business.text}
                        </ToggleButton>})}
                </ToggleButtonGroup>
                <Box textAlign='center' mb='0.5rem' mt='0.5rem'>
                    <Button variant="contained" color='primary'>
                        Apply the Filter
                    </Button>
                </Box>
                <Box textAlign='center' mb='0.5rem'>
                    <Button variant="contained" color='primary-subtle'>
                        Reset the Filter
                    </Button>
                </Box>
            </BootstrapDialog>
        </Paper>
    )
}

export default Landingpages