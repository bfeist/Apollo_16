import { createSlice } from "@reduxjs/toolkit";
import { PhotosState } from "../typings";

export const initialState: PhotosState = {
  photosFlight: [],
};

export const photoSlice = createSlice({
  name: "photo",
  initialState,
  reducers: {
    /** Add new photo files to the store */
    addPhotosFlight: (state, action) => {
      state.photosFlight = action.payload;
    },
  },
});

export const { addPhotosFlight } = photoSlice.actions;

/** Filters photos for a given day */
// const _filterVisiblePhotos = (photos: PhotoFile[], date: Date): PhotoFile[] => {
//   return photos.filter((photo) => {
//     return isSameDate(new Date(photo.datetimeTaken), date);
//   });
// };

// /** Return a list of all photos for a given day */
// export const filterVisiblePhotos = memoize(
//   _filterVisiblePhotos,
//   (photos: PhotoFile[], date: Date) => `${photos.length}/${date.toISOString()}`
// );
