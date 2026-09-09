import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import styles from "./Navbar.module.css";

export default function Navbar({ onNavigate = () => {}, onRequestOpportunity = () => {} }) {
  const [open, setOpen] = useState(false);
  const { user, loading, signOut } = useAuth();
  const go = (path, anchor) => { setOpen(false); if (path) onNavigate(path); if (anchor && window.location.pathname === "/") setTimeout(() => document.querySelector(anchor)?.scrollIntoView({ behavior: "smooth" }), 0); };
  const find = () => { setOpen(false); onRequestOpportunity(); };
  return <header className={styles.header}><nav className={styles.nav} aria-label="Main navigation"><button className={styles.brand} onClick={() => go("/")}>SIMT <span>AI</span></button><button className={styles.menu} onClick={() => setOpen(!open)} aria-expanded={open} aria-label="Toggle navigation">{open ? "×" : "☰"}</button><div className={`${styles.links} ${open ? styles.open : ""}`}><button onClick={() => go("/")}>Home</button><button onClick={() => go("/", "#how-it-works")}>How it works</button><button onClick={() => go("/", "#faq")}>FAQ</button>{user ? <button className={styles.account} onClick={() => signOut()}>Log out</button> : <button className={styles.login} onClick={find} disabled={loading}>Login / Sign Up</button>}<button className={styles.cta} onClick={find} disabled={loading}>Find opportunities</button></div></nav></header>;
}
