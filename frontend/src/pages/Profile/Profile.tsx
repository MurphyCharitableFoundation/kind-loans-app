import * as React from "react";
import { useForm } from "react-hook-form";
import {
  Box,
  Button,
  FormControl,
  Input,
  MenuItem,
  Select,
  Stack,
  Avatar,
} from "@mui/material";
import UploadWidget from "../../components/UploadWidget";
// import { AdvancedImage, responsive, placeholder } from "@cloudinary/react";
import Cookies from "js-cookie";

export type profileType = {
  business_name: string;
  business_type: string;
  city: number;
  country: number;
  email: string;
  interests: string;
  name: string;
  photoURL: string;
  role: string;
  story: string;
};

export default function Profile() {
  const [imageId, setImageId] = React.useState<string>("");
  const [profileList, setProfileList] = React.useState<profileType>({
    business_name: "",
    business_type: "",
    city: 0,
    country: 0,
    email: "",
    interests: "",
    name: "",
    photoURL: "",
    role: "",
    story: "",
  });
  const [editMode, setEditMode] = React.useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const fetchProfileData = (data: any): void => {
    const param: any = data
      ? {
          method: "PATCH",
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken")!,
            Authorization: `Token ${Cookies.get("token")}`,
          },
          body: JSON.stringify({ ...data, photoURL: imageId }),
        }
      : {
          method: "GET",
          headers: {
            accept: "application/json",
            "X-CSRFToken": Cookies.get("csrftoken")!,
            Authorization: `Token ${Cookies.get("token")}`,
          },
        };

    fetch("api/user/me/", param)
      .then((data) => {
        if (!data.ok) {
          throw new Error("error");
        }
        return data.json();
      })
      .then((data) => {
        setProfileList({ ...data });
        setEditMode(false);
        setImageId(data.photoURL);
        scrollTo(0, 0);
      })
      .catch((error) => console.error("error", error));
  };

  const generateFormElement = (name: string): JSX.Element => {
    if (name == "role" || name == "country" || name == "city") {
      const obj: { [key: string | number]: string } =
        name == "role"
          ? {
              borrower: "Borrower",
              lender: "Lender",
              admin: "Admin",
            }
          : name == "country"
          ? {
              1: "Canada",
              2: "England",
              3: "Australia",
            }
          : {
              1: "Vancouver",
              2: "London",
              3: "Paris",
            };

      return (
        <FormControl>
          <Select defaultValue={profileList[name]} {...register(name)}>
            {Object.keys(obj).map((key, index) => {
              return (
                <MenuItem key={index} value={key}>
                  {obj[key]}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      );
    } else {
      return (
        <Box>
          <Input
            defaultValue={profileList[name as keyof typeof profileList]}
            {...register(name, { required: "This field is required." })}
          />
          <Box color="red">{errors[name]?.message?.toString()}</Box>
        </Box>
      );
    }
  };

  React.useEffect(() => {
    fetchProfileData(null);
  }, []);

  return (
    <Box
      sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <Box
        sx={{ margin: "20px", width: 150, height: 150, position: "relative" }}
      >
        <Avatar
          alt="Remy Sharp"
          src={imageId}
          sx={{ width: "100%", height: "100%" }}
        />

        {!editMode && (
          <Avatar
            alt="Edit"
            src="https://img.icons8.com/?size=100&id=3dbDiCK5fTtx&format=png&color=00000077"
            onClick={() => setEditMode(true)}
            sx={{
              height: 40,
              width: 40,
              background: "#cccccc",
              padding: "5px",
              position: "absolute",
              right: 0,
              bottom: 0,
              cursor: "pointer",
            }}
          />
        )}
      </Box>

      {editMode && (
        <UploadWidget setImageId={setImageId} setProfileList={setProfileList} />
      )}
      <Box
        component="form"
        onSubmit={handleSubmit((data: any) => fetchProfileData(data))}
      >
        <Stack>
          {Object.keys(profileList).map(
            (key: string, index: number) =>
              key !== "photoURL" && (
                <Box
                  key={index}
                  sx={{
                    borderTop: `${editMode ? "none" : "1px solid #00000033"}`,
                    padding: "12px 16px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <Box sx={{ width: "120px", color: "#00000077" }}>{key}</Box>

                  {editMode ? (
                    generateFormElement(key)
                  ) : (
                    <Box>{profileList[key as keyof typeof profileList]}</Box>
                  )}
                </Box>
              )
          )}
        </Stack>
        {editMode && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Button type="submit" variant="outlined">
              Save
            </Button>
          </Box>
        )}
      </Box>
    </Box>
  );
}
