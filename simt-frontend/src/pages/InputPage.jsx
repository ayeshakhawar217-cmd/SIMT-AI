import Navbar from "../components/Navbar";
import SituationInput from "../components/SituationInput";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import { submitSituation } from "../services/api";
import styles from "./InputPage.module.css";
import { useState } from "react";
export default function InputPage({ onComplete, onHome }) { const [loading, setLoading] = useState(false); const [error, setError] = useState(false); const [lastSituation, setLastSituation] = useState(""); const submit = async (situation) => { setLastSituation(situation); setLoading(true); setError(false); try { onComplete(await submitSituation(situation)); } catch { setError(true); } finally { setLoading(false); } }; return <><Navbar onNavigate={(path) => path === "/" ? onHome() : null} /><main className={styles.page}>{loading ? <LoadingState /> : error ? <ErrorState onRetry={() => lastSituation ? submit(lastSituation) : setError(false)} /> : <SituationInput onSubmit={submit} />}</main></>; }
