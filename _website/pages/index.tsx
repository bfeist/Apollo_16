import Head from "next/head";
import Link from "next/link";
import styles from "./index.module.css";

export default function Index() {
  return (
    <div className={styles.container}>
      <Head>
        <title>{process.env.TITLE}</title>
      </Head>
      Hello.
    </div>
  );
}
