import Head from "next/head";
import styles from "./index.module.css";
import { server } from "../config";
import { RootState } from "store";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { addPhotosFlight } from "store/photos";
import type { PhotoFlight } from "typings";
import WithPlayheadWrapper from "components/playheadWrapper";

function Index(props) {
  const dispatch = useDispatch();
  const photos = useSelector((state: RootState) => state.photos);

  useEffect(() => {
    const photosFlight: PhotoFlight[] = props.photosFlightArray.map((arrayItem) => {
      const [GETTimestamp, filenameRoot] = arrayItem;
      return { GETTimestamp, filenameRoot };
    });
    dispatch(addPhotosFlight(photosFlight));
  }, [dispatch]);

  return (
    <div className={styles.container}>
      <Head>
        <title>{process.env.TITLE}</title>
      </Head>
      Data length: {photos.photosFlight.length}
    </div>
  );
}

export default WithPlayheadWrapper(Index);

export async function getStaticProps() {
  const res = await fetch(`${server}/indexes/a16_photos_flight.csv`);
  const photoLines = await (await res.text()).split("\n");
  const photosFlightArray = photoLines.map((line) => {
    const [GETTimestamp, filenameRoot] = line.split("|");
    if (GETTimestamp && filenameRoot) {
      return [GETTimestamp, filenameRoot];
    } else {
      return null;
    }
  });

  return {
    props: { photosFlightArray },
  };
}
