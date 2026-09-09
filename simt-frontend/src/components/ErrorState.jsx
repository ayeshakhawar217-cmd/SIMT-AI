import styles from "./ErrorState.module.css";
export default function ErrorState({ onRetry }) { return <div className={styles.state} role="alert"><div>!</div><h1>We couldn’t connect to SIMT right now.</h1><p>Please make sure the backend is running and try again.</p><button onClick={onRetry}>Try Again</button></div>; }
