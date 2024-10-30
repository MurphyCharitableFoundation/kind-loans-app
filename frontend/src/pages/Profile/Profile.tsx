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
import profilePic from "../../assets/dummypic.png";
import Cookies from "js-cookie";

export default function Profile() {
  const [profileList, setProfileList] = React.useState<any>({});
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
          body: JSON.stringify({ ...data }),
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
        scrollTo(0, 0);
      })
      .catch((error) => console.error("error", error));
  };

  const generateFormElement = (name: string): JSX.Element => {
    if (name == "role" || name == "country" || name == "city") {
      const obj: any =
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
            defaultValue={profileList[name]}
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
          src={profilePic}
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

      <Box
        component="form"
        onSubmit={handleSubmit((data: any) => fetchProfileData(data))}
      >
        <Stack>
          {Object.keys(profileList).map((key: string, index: number) => (
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
                <Box>{profileList[key]}</Box>
              )}
            </Box>
          ))}
        </Stack>
        {editMode && (
          <Button
            type="submit"
            sx={{
              border: "1px solid #00000055",
              margin: "0 auto",
              display: "block",
            }}
          >
            Save
          </Button>
        )}
      </Box>
    </Box>
  );
}
