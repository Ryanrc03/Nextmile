"use client";

import { useState } from "react";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false); // 默认收起状态
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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div
      className="fixed bottom-6 right-6 z-50"
    >
      {isOpen ? (
        <div className="bg-[#1a1a1a] border border-gray-700 text-white rounded-2xl shadow-2xl backdrop-blur-sm"
             style={{ width: "350px", height: "450px" }}>
          
          {/* Header */}
          <div className="flex justify-between items-center p-4 border-b border-gray-700">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-[#00D9FF] rounded-full flex items-center justify-center">
                <span className="text-black font-bold text-sm">AI</span>
              </div>
              <h2 className="text-lg font-bold text-white">Chat Assistant</h2>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-white transition-colors p-1"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className="h-80 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
            {messages.length === 0 ? (
              <div className="text-center text-gray-400 mt-8">
                <div className="text-4xl mb-2">👋</div>
                <p>Hello! I'm your AI assistant.</p>
                <p className="text-sm">How can I help you today?</p>
              </div>
            ) : (
              messages.map((msg, index) => {
                const isUser = msg.startsWith('You:');
                const content = msg.replace(/^(You:|AI:)\s*/, '');
                
                return (
                  <div key={index} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                      isUser 
                        ? 'bg-[#00D9FF] text-black' 
                        : 'bg-[#2a2a2a] text-white border border-gray-600'
                    }`}>
                      {content}
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-700">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1 bg-[#2a2a2a] border border-gray-600 text-white rounded-lg px-3 py-2 text-sm placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors"
                placeholder="Type your message..."
              />
              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className="bg-[#00D9FF] hover:bg-[#00B8CC] disabled:bg-gray-600 disabled:cursor-not-allowed text-black px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-[#00D9FF] hover:bg-[#00B8CC] text-black rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-[#00D9FF]"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
          </svg>
        </button>
      )}
    </div>
  );
}
