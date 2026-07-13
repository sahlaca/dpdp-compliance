import { useState } from "react";
import { LoginPage } from "./LoginPage";
import { MainApp } from "./MainApp";
import { getUser, type AuthUser } from "./auth";
import "./App.css";

export default function App() {
  const [user, setUser] = useState<AuthUser | null>(() => getUser());

  if (!user) {
    return <LoginPage onSuccess={setUser} />;
  }

  return <MainApp user={user} onLogout={() => setUser(null)} />;
}
