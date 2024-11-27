import { createSlice } from "@reduxjs/toolkit";
import { Cloudinary } from "@cloudinary/url-gen";

export interface CloudinarySate {
  myCld: Cloudinary;
}

const initialState: CloudinarySate = {
  myCld: new Cloudinary({
    cloud: {
      cloudName: "dqlx6iqqt",
    },
  }),
};

export const CloudinarySate = createSlice({
  name: "cloudinary",
  initialState,
  reducers: {},
});

export default CloudinarySate.reducer;
