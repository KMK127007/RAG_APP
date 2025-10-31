import React from "react";
import AskForm from "./components/AskForm";

export default function App() {
  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem", textAlign: "center" }}>
      <h1>🧠 Generative AI Math Q&A</h1>
      <AskForm />
    </div>
  );
}
