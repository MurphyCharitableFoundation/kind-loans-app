import Popover from "@mui/material/Popover";
import * as React from 'react';
import Box from '@mui/material/Box';
import FilterListIcon from '@mui/icons-material/FilterList';
import IconButton from '@mui/material/IconButton';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';


const Radio_Buttons = [
    {value:"cloest deadline",label:"Cloest Deadline"},
    {value:"recent upload",label:"Recent Upload"},
    {value:"low to high",label:"Total Amount: Low to high"},
    {value:"high to low",label:"Total Amount: High to low"}
]


function SortFilterPopover(props){
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const [value,setValue] = React.useState("cloest deadline")

    
    const handleRadioChange = (event) =>{
        setValue((event.target as HTMLInputElement).value);
    }

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
      };
    
    const handleClose = () => {
        setAnchorEl(null);
      };
    const open = Boolean(anchorEl);
    const id = open ? 'sort-filter-popper' : undefined;
    
    return (
        <Box>
            <IconButton aria-label="Sort" onClick={handleClick} >
                <FilterListIcon />
            </IconButton>
            <Popover 
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                PaperProps={{
                    style: {
                      backgroundColor: "transparent",
                      boxShadow: "none",
                      borderRadius: 0,
                    },
                  }}>
                <Box
                    sx={{
                        position: "relative",
                        mt: "10px",
                        "&::before": {
                        backgroundColor: "white",
                        content: '""',
                        display: "block",
                        position: "absolute",
                        width: 12,
                        height: 12,
                        top: -6,
                        borderTop:1,
                        borderLeft:1,
                        transform: "rotate(45deg)",
                        left: "calc(90% - 6px)",
                        zIndex:10000
                        },
                    }}
                />
                <Box sx={{backgroundColor:"white",p:1,borderRadius:1,border:1,zIndex:1000}}>
                    <FormControl>
                        <FormLabel id="sort-radio-buttons-group-label">Sort by:</FormLabel>
                        <RadioGroup
                            aria-labelledby="sort-radio-buttons-group-label"
                            defaultValue={value}
                            name="radio-buttons-group"
                            onChange={handleRadioChange}
                        >   
                            {Radio_Buttons.map( (item,i) => <FormControlLabel key={i} value={item.value} control={<Radio />} label={item.label} />)}
                        </RadioGroup>
                    </FormControl>
                </Box>
            </Popover>
           

        </Box>
)
}

export default SortFilterPopover