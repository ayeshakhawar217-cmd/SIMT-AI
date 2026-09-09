import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import styles from "./AuthModal.module.css";

const cleanError = (message) => {
  const value = message?.toLowerCase() || "";
  if (value.includes("invalid login") || value.includes("invalid credentials")) return "Invalid email or password.";
  if (value.includes("password")) return "Password is too weak. Please choose a stronger password.";
  if (value.includes("email")) return "Please enter a valid email address.";
  return "Something went wrong. Please try again.";
};

export default function AuthModal({ onClose, onAuthenticated }) {
  const { configured, signIn, signUp } = useAuth();
  const [mode, setMode] = useState("login"); const [email, setEmail] = useState(""); const [password, setPassword] = useState(""); const [confirmPassword, setConfirmPassword] = useState(""); const [error, setError] = useState(""); const [notice, setNotice] = useState(""); const [submitting, setSubmitting] = useState(false);
  const signingUp = mode === "signup";
  const changeMode = () => { setMode(signingUp ? "login" : "signup"); setError(""); setNotice(""); };
  const submit = async (event) => {
    event.preventDefault(); setError(""); setNotice("");
    if (!configured) { setError("Authentication is not configured yet. Please add the Supabase environment variables."); return; }
    if (signingUp && password !== confirmPassword) { setError("Passwords do not match."); return; }
    setSubmitting(true);
    const { data, error: authError } = signingUp ? await signUp(email, password) : await signIn(email, password);
    setSubmitting(false);
    if (authError) { setError(cleanError(authError.message)); return; }
    if (data.session) { onAuthenticated(); return; }
    if (signingUp) setNotice("Check your email to confirm your account, then log in to continue.");
  };
  return <div className={styles.backdrop} role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}><section className={styles.modal} role="dialog" aria-modal="true" aria-labelledby="auth-title"><button className={styles.close} onClick={onClose} aria-label="Close authentication">×</button><span className={styles.eyebrow}>SIMT <b>AI</b></span><h2 id="auth-title">{signingUp ? "Create your account" : "Welcome back"}</h2><p className={styles.intro}>{signingUp ? "Save your place and start finding relevant opportunities." : "Log in to continue finding your opportunities."}</p><form onSubmit={submit}><label>Email<input type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label><label>Password<input type="password" autoComplete={signingUp ? "new-password" : "current-password"} value={password} onChange={(event) => setPassword(event.target.value)} minLength="6" required /></label>{signingUp && <label>Confirm Password<input type="password" autoComplete="new-password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} minLength="6" required /></label>}{error && <p className={styles.error} role="alert">{error}</p>}{notice && <p className={styles.notice} role="status">{notice}</p>}<button className={styles.submit} disabled={submitting}>{submitting ? "Please wait…" : signingUp ? "Create Account" : "Log In"}</button></form><p className={styles.switch}>{signingUp ? "Already have an account?" : "Don't have an account?"} <button onClick={changeMode}>{signingUp ? "Log in" : "Sign up"}</button></p></section></div>;
}
