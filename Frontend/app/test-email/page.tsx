"use client";

import { useState } from "react";

export default function EmailTest() {
  const [result, setResult] = useState<string>("");

  const testEmail = async () => {
    setResult("Testing...");
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          firstName: "Test",
          lastName: "User",
          emailId: "test@example.com",
          mobNo: "123-456-7890",
          message: "This is a test message from the contact form."
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setResult(`✅ Success: ${JSON.stringify(data, null, 2)}`);
      } else {
        setResult(`❌ Error: ${JSON.stringify(data, null, 2)}`);
      }
    } catch (error) {
      setResult(`❌ Network Error: ${error}`);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Email Test Page</h1>
        
        <button
          onClick={testEmail}
          className="bg-[#00D9FF] text-black px-6 py-3 rounded-lg font-semibold mb-8"
        >
          Test Email Sending
        </button>
        
        <div className="bg-[#1a1a1a] p-6 rounded-lg">
          <h2 className="text-xl font-bold mb-4">Result:</h2>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
        
        <div className="mt-8 bg-[#2a2a2a] p-6 rounded-lg">
          <h2 className="text-xl font-bold mb-4">Environment Check:</h2>
          <p>Email User: {process.env.EMAIL_USER ? "✅ Set" : "❌ Missing"}</p>
          <p>Email Pass: {process.env.EMAIL_PASS ? "✅ Set" : "❌ Missing"}</p>
        </div>
      </div>
    </div>
  );
}