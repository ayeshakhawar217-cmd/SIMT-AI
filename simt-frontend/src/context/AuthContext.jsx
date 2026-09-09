import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { isSupabaseConfigured, supabase } from "../lib/supabase";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isSupabaseConfigured) { setLoading(false); return undefined; }
    let active = true;
    supabase.auth.getSession().then(({ data: { session: nextSession } }) => {
      if (!active) return;
      setSession(nextSession); setUser(nextSession?.user ?? null); setLoading(false);
    }).catch(() => active && setLoading(false));
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession); setUser(nextSession?.user ?? null); setLoading(false);
    });
    return () => { active = false; subscription.unsubscribe(); };
  }, []);

  const value = useMemo(() => ({ user, session, loading, configured: isSupabaseConfigured,
    signUp: (email, password) => supabase.auth.signUp({ email, password }),
    signIn: (email, password) => supabase.auth.signInWithPassword({ email, password }),
    signOut: () => supabase.auth.signOut(),
  }), [user, session, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error("useAuth must be used inside AuthProvider"); return value; }
