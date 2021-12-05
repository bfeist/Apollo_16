import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { playheadSlice, initialState as playheadInitialState } from "./playhead";
import { playheadHoverSlice, initialState as playheadHoverInitialState } from "./playheadHover";
import { photoSlice, initialState as photosInitialState } from "./photos";

export const initialState = {
  playhead: playheadInitialState,
  playheadHover: playheadHoverInitialState,
  photos: photosInitialState,
};

const reducer = combineReducers({
  playhead: playheadSlice.reducer,
  playheadHover: playheadHoverSlice.reducer,
  photos: photoSlice.reducer,
});

export type RootState = ReturnType<typeof reducer>;

const store = configureStore({
  reducer,
  devTools: true,
});
export default store;
