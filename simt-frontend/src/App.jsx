import { useEffect, useState } from "react";
import LandingPage from "./pages/LandingPage";
import InputPage from "./pages/InputPage";
import ResultsPage from "./pages/ResultsPage";
import ProgramDetailPage from "./pages/ProgramDetailPage";
import AuthModal from "./components/AuthModal";
import { useAuth } from "./context/AuthContext";

const getRoute = () => window.location.pathname;
export default function App() {
  const [route, setRoute] = useState(getRoute()); const [result, setResult] = useState(null); const [authOpen, setAuthOpen] = useState(false);
  const { user, loading } = useAuth();
  useEffect(() => { const onPop = () => setRoute(getRoute()); window.addEventListener("popstate", onPop); return () => window.removeEventListener("popstate", onPop); }, []);
  const navigate = (path) => { window.history.pushState({}, "", path); setRoute(path); window.scrollTo(0, 0); };
  const reset = () => { setResult(null); navigate("/input"); };
  const requestOpportunity = () => { if (loading) return; if (user) navigate("/input"); else setAuthOpen(true); };
  let page;
  if (route.startsWith("/program/")) { const id = decodeURIComponent(route.split("/").pop()); const match = result?.matches?.find((item, index) => String(item?.id ?? index) === id); page = <ProgramDetailPage match={match} onBack={() => navigate("/results")} onNewSearch={reset} />; }
  else if (route === "/input") page = <InputPage onComplete={(data) => { setResult(data); navigate("/results"); }} onHome={() => navigate("/")} />;
  else if (route === "/results") page = <ResultsPage data={result} onProgram={(match, index) => navigate(`/program/${encodeURIComponent(match?.id ?? index)}`)} onNewSearch={reset} />;
  else page = <LandingPage onNavigate={navigate} onRequestOpportunity={requestOpportunity} />;
  return <>{page}{authOpen && <AuthModal onClose={() => setAuthOpen(false)} onAuthenticated={() => { setAuthOpen(false); navigate("/input"); }} />}</>;
}
