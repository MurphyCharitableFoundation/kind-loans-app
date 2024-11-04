import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit"
import Cookies from "js-cookie";

export interface AuthState {
  token: string | null;
}

const initialState: AuthState = {
  token: Cookies.get("token") || null,
};

export const AuthState = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setToken: (state, action: PayloadAction<string | null>) => {
      state.token = action.payload;
    },
  },
});

export const { setToken } = AuthState.actions;

export default AuthState.reducer;
