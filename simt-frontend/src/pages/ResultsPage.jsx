import Navbar from "../components/Navbar";
import ProfileSummary from "../components/ProfileSummary";
import MatchList from "../components/MatchList";
import styles from "./ResultsPage.module.css";
export default function ResultsPage({ data, onProgram, onNewSearch }) { const matches = Array.isArray(data?.matches) ? data.matches : []; return <><Navbar onNavigate={() => onNewSearch()} /><main className={styles.page}><div className={styles.heading}><span className={styles.eyebrow}>Your direction</span><h1>Opportunities for you</h1><p>These results are based on the situation you shared. Review each option and its eligibility details before applying.</p></div><ProfileSummary profile={data?.profile} /><MatchList matches={matches} onProgram={onProgram} onNewSearch={onNewSearch} /></main></>; }
