import { useMemo } from "react";
import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { playheadSlice, initialState as playheadInitialState } from "./playhead";
import { playheadHoverSlice, initialState as playheadHoverInitialState } from "./playheadHover";

let store;

export const initialState = {
  playhead: playheadInitialState,
  playheadHover: playheadHoverInitialState,
};

// server-side redux technique adapted from https://github.com/vercel/next.js/blob/canary/examples/with-redux/store.js#L50

const reducer = combineReducers({
  playhead: playheadSlice.reducer,
  playheadHover: playheadHoverSlice.reducer,
});

export type RootState = ReturnType<typeof reducer>;

const initStore = (preloadedState = initialState) => {
  const store = configureStore({
    reducer,
    preloadedState,
    devTools: true,
  });
  return store;
};

export const initializeStore = (preloadedState) => {
  let _store = store ?? initStore(preloadedState);

  // After navigating to a page with an initial Redux state, merge that state
  // with the current state in the store, and create a new store
  if (preloadedState && store) {
    _store = initStore({
      ...store.getState(),
      ...preloadedState,
    });
    // Reset the current store
    store = undefined;
  }

  // For SSG and SSR always create a new store
  if (typeof window === "undefined") return _store;
  // Create the store once in the client
  if (!store) store = _store;

  return _store;
};

export function useStore(initialState) {
  store = useMemo(() => initializeStore(initialState), [initialState]);
  return store;
}
