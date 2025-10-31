import React, { useState } from "react";

export default function AskForm() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer("Please enter a question first!");
      return;
    }

    setAnswer("Loading...");
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, user_id: "murali" }),
      });

      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setAnswer(data.answer || "No answer found in knowledge base.");
    } catch (err) {
      setAnswer("❌ Network error — check if backend is running on port 8000.");
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a math question..."
        style={{ padding: "0.5rem", width: "60%" }}
      />
      <button
        onClick={handleAsk}
        style={{
          padding: "0.5rem 1rem",
          marginLeft: "0.5rem",
          background: "blue",
          color: "white",
          border: "none",
          borderRadius: "4px",
        }}
      >
        Ask
      </button>

      {answer && (
        <div style={{ marginTop: "1.5rem", fontSize: "1.1rem", color: "#333" }}>
          <strong>Answer:</strong> {answer}
        </div>
      )}
    </div>
  );
}
