import Carousel from 'react-material-ui-carousel'
import BorrowerCard from './BorrowerCard'

const LoanPofileTest = [
    {
        imgPath: "../../../public/lilac_nature_flower_purple.jpg",
        loanDescription: "“ I’m a 32-year old mother of three with a dream to build my own tailoring business so I can support my family.”",
        localtionDescription:"-Monal, Clothing shop owner in Uganda"
    },
    {
        imgPath: "../../../public/lilac_blossom_bloom_white_0.jpg",
        loanDescription: "“ I’m a 33-year old mother of three with a dream to build my own tailoring business so I can support my family.”",
        localtionDescription:"-Monal, Clothing shop owner in Uganda"
    },
    {
        imgPath: "../../../public/lilac_flower_spring_blossom.jpg",
        loanDescription: "“ I’m a 34-year old mother of three with a dream to build my own tailoring business so I can support my family.”",
        localtionDescription:"-Monal, Clothing shop owner in Uganda"
    }
]


function LandPageCarousel(){
    return (
        <Carousel 
        navButtonsAlwaysVisible={true}
        activeIndicatorIconButtonProps={{
            style: {
                border: "transparent",
                backgroundColor: "transparent"
            }
        }}
        indicatorIconButtonProps={{
            style: {
                border: "transparent"
            }
        }}
        animation={"slide"}
        duration={800}
        >
            {
                LoanPofileTest.map( (item, i) => <BorrowerCard key={i} LoanPofile={item} /> )
            }
        </Carousel>
    )
}


export default LandPageCarousel