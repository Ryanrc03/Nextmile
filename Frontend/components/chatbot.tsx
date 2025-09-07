"use client";

import { useState } from "react";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(true); // 控制 Chatbot 的展开/收起状态
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, `You: ${input}`]);

      try {
        console.log("Sending request to backend...");
        const response = await fetch("http://127.0.0.1:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: input,
          }),
        });

        console.log("Response status:", response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log("Response data:", data);
          setMessages((prev) => [...prev, `AI: ${data.reply}`]);
        } else {
          const errorText = await response.text();
          console.error("Response error:", errorText);
          setMessages((prev) => [...prev, `AI: Error - Failed to get response. Status: ${response.status}`]);
        }
      } catch (error) {
        console.error("Fetch error:", error);
        setMessages((prev) => [...prev, `AI: Error connecting to server: ${error.message}`]);
      }

      setInput("");
    }
  };

  return (
    <div
      className="fixed bottom-5 right-5"
      style={{ zIndex: 1000 }} // 确保 Chatbot 在最上层
    >
      {isOpen ? (
        <div
          className="bg-gray-200 text-black rounded-lg shadow-lg p-4"
          style={{ width: "300px", height: "400px" }}
        >
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-lg font-bold">Chatbot</h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Close
            </button>
          </div>
          <div
            className="h-64 overflow-y-auto border border-gray-300 rounded p-2 mb-2"
            style={{ backgroundColor: "#f9f9f9" }}
          >
            {messages.map((msg, index) => (
              <p key={index} className="text-sm">
                {msg}
              </p>
            ))}
          </div>
          <div className="flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 border border-gray-300 rounded p-2 text-sm"
              placeholder="Type a message..."
            />
            <button
              onClick={handleSend}
              className="ml-2 bg-gray-800 text-white px-3 py-1 rounded text-sm"
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gray-800 text-white rounded-full w-12 h-12 flex items-center justify-center"
        >
          💬
        </button>
      )}
    </div>
  );
}
