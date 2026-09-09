import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import HowItWorks from "../components/HowItWorks";
import FAQ from "../components/FAQ";
import Footer from "../components/Footer";
import CreditsBar from "../components/CreditsBar";
export default function LandingPage({ onNavigate, onRequestOpportunity }) { return <><Navbar onNavigate={onNavigate} onRequestOpportunity={onRequestOpportunity} /><main><Hero onStart={onRequestOpportunity} /><Features /><HowItWorks /><FAQ /></main><Footer onNavigate={onNavigate} /><CreditsBar /></>; }
