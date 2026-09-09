import { useEffect, useState } from "react";
import styles from "./LoadingState.module.css";
const messages = ["Analyzing your situation…", "Finding relevant opportunities…", "Checking eligibility…", "Preparing your direction…"];
export default function LoadingState() { const [index, setIndex] = useState(0); useEffect(() => { const id = setInterval(() => setIndex((value) => Math.min(value + 1, messages.length - 1)), 1300); return () => clearInterval(id); }, []); return <div className={styles.state} role="status"><div className={styles.loader}></div><span>SIMT AI is working</span><h1>{messages[index]}</h1><p>This should only take a moment.</p></div>; }
