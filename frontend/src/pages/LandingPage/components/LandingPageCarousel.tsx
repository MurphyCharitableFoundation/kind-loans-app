import BorrowerCard from './BorrowerCard'
import Box from "@mui/material/Box";
import {Swiper, SwiperSlide} from "swiper/react";
import {Navigation} from "swiper/modules";
import {NextIcon, PrevIcon} from "../../../assets/icons.tsx";
import "swiper/css";
import 'swiper/css/navigation';
import Button from "@mui/material/Button";
import {useQuery} from "@tanstack/react-query";
import LoanProfile from "../../../types/LoanProfile";
import {Error} from "@mui/icons-material";

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
    const { data, error, isLoading } = useQuery<LoanProfile[]>({
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

    console.log(data)

    return (
        <Box sx={{display: "flex",justifyContent: "space-between",alignItems: "center",width: "100%"}}>
            <Button className="custom-prev">
                <PrevIcon color="green" />
            </Button>
            <Swiper
                    navigation={{
                        enabled: true,
                        nextEl: ".custom-next",
                        prevEl: ".custom-prev",
                    }} modules={[Navigation]} loop={true}
            >
                {data?.map((item,i) => (
                    <SwiperSlide key={i}>
                        <div key={i}
                             style={{
                                 display: "flex",
                                 justifyContent: "center",
                                 alignItems: "center",
                             }}
                        >
                            <BorrowerCard key={i} imgPath={item.profile_img} loanDescription={item.description} location={item.title} />
                        </div>
                    </SwiperSlide>
                ))}
            </Swiper>
            <Button className="custom-next">
                <NextIcon color="green"/>
            </Button>
        </Box>
    )
}


export default LandPageCarousel
