import type { AppProps } from "next/app";
import { Provider } from "react-redux";
import store from "store";
import "../styles.css";

// This default export is required in a new `pages/_app.js` file.
export default function App({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
