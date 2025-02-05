import React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Button from '@mui/material/Button';
import { Box } from "@mui/material";
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import ToggleButtonGroupForBusinesses from './ToggleButtonForBusinesses';
const FilterButtonBusinesses = [{id:1,text:"Any business type"} , {id:2,text:"Medical"} , {id:3,text:"Colthing"} ,{id:4,text:"Grocery"}, {id:5,text:"Emergency"},{id:6,text:"Education"},{id:7,text:"Others"}]

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
      padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
      padding: theme.spacing(1),
    },
  }));

function SearchDialog(props){
    // need handle apply here
    const [business, setBusiness] = React.useState(() => []);

    const handleBusiness = (event, newBusiness) => {
      setBusiness(newBusiness);
    };

    function handleReset(){
        setBusiness([])
    }

    return (
    <BootstrapDialog
    onClose={props.handleClose}
    aria-labelledby="customized-dialog-title"
    open={props.open}
    fullWidth={true}
    maxWidth={"sm"}
    >
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
        Filter - Loan Search
        </DialogTitle>
        {/* should have some paddings here */}
        <Box textAlign="center">
            <Typography variant="body2" gutterBottom>
            I want to support someone with a loan for
            </Typography>
        </Box>
        <ToggleButtonGroupForBusinesses 
        FilterButtonBusinesses={FilterButtonBusinesses}
        business={business}
        handleBusiness={handleBusiness}/>
        {/* <ToggleButtonGroup value={props.business} onChange={props.handleBusiness} sx={{ flexWrap: "wrap"}}>
            {FilterButtonBusinesses.map((business) => {
                return <ToggleButton 
                        key={business.id} 
                        value={business.text}
                        sx={{ margin: 2,"&.Mui-selected, &.Mui-selected:hover": {backgroundColor: '#07001C!important'}}}
                        style={{borderRadius: '12px', color:'#FFFFFF',backgroundColor: '#A3A3A3'}}
                        >
                    {business.text}
                </ToggleButton>})}
        </ToggleButtonGroup> */}
        <Box textAlign='center' mb='0.5rem' mt='0.5rem'>
            <Button variant="contained" color='primary'>
                Apply the Filter
            </Button>
        </Box>
        <Box textAlign='center' mb='0.5rem'>
            <Button variant="contained" color='primary-subtle' onClick={handleReset}>
                Reset the Filter
            </Button>
        </Box>
    </BootstrapDialog>
    )
}

export default SearchDialog