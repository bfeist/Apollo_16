import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { run, halt, tick } from "../store/playhead";
import useInterval from "utils/useInterval";
import { RootState } from "../store/index";

function PlayheadWrapper() {
  const playheadReady = useSelector((state: RootState) => state.playhead.ready);
  const playheadIsRunning = useSelector((state: RootState) => state.playhead.isRunning);

  const dispatch = useDispatch();

  useEffect(() => {
    if (playheadReady && !playheadIsRunning) {
      dispatch(run());
    } else if (!playheadReady && playheadIsRunning) {
      dispatch(halt());
    }
  }, [playheadReady, playheadIsRunning, dispatch]);

  useInterval(() => {
    if (playheadIsRunning) {
      dispatch(tick());
    }
  }, 1000);

  return <></>;
}

export default function WithPlayheadWrapper<P>(Component: React.ComponentType<P>) {
  return ({ ...props }) => {
    return (
      <>
        <PlayheadWrapper />
        <Component {...(props as P)} />
      </>
    );
  };
}
