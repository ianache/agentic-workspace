"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Bot, User, Database, RefreshCw } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "¡Hola! Soy tu Agente Analítico de IA. ¿En qué puedo ayudarte hoy con tus datos?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/ask", {
        question: input,
        history: messages.map(m => ({ role: m.role, content: m.content }))
      });

      const botMessage: Message = { role: "assistant", content: response.data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error calling API:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Lo siento, hubo un error al procesar tu solicitud. Asegúrate de que el backend esté ejecutándose." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-blue-700 text-white shadow-md p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-6 h-6" />
          <h1 className="text-xl font-bold">Agente Analítico de IA</h1>
        </div>
        <div className="text-sm bg-blue-600 px-3 py-1 rounded-full flex items-center gap-2">
          <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
          {isLoading ? 'Analizando...' : 'Conectado'}
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4" ref={scrollRef}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] flex gap-3 p-4 rounded-2xl shadow-sm ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-none"
                  : "bg-white text-gray-800 border border-gray-200 rounded-tl-none"
              }`}
            >
              <div className="mt-1 shrink-0">
                {msg.role === "user" ? <User size={18} /> : <Bot size={18} className="text-blue-600" />}
              </div>
              <div className="overflow-x-auto w-full">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    table: ({node, ...props}) => (
                      <div className="overflow-x-auto my-2">
                        <table className="border-collapse border border-gray-300 w-full text-sm" {...props} />
                      </div>
                    ),
                    th: ({node, ...props}) => <th className="border border-gray-300 px-2 py-1 bg-gray-100 font-bold" {...props} />,
                    td: ({node, ...props}) => <td className="border border-gray-300 px-2 py-1" {...props} />,
                    p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc ml-4 mb-2" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal ml-4 mb-2" {...props} />,
                    li: ({node, ...props}) => <li className="mb-1" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-bold text-blue-800 dark:text-blue-300" {...props} />,
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white p-4 rounded-2xl border border-gray-100 flex gap-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.4s]" />
            </div>
          </div>
        )}
      </main>

      {/* Input Area */}
      <footer className="p-4 bg-white border-t border-gray-200">
        <div className="max-w-4xl mx-auto flex gap-2 items-center">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-full py-3 px-6 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-gray-800"
            placeholder="Haz una pregunta sobre tus datos (ej. ¿Cúal fue el producto más vendido?)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            className="bg-blue-700 text-white p-3 rounded-full hover:bg-blue-800 disabled:opacity-50 transition-colors shadow-lg"
            disabled={isLoading || !input.trim()}
          >
            <Send className="w-6 h-6" />
          </button>
        </div>
        <p className="text-center text-xs text-gray-400 mt-2">
          Versión 1.0 - Powered by Vertex AI & BigQuery
        </p>
      </footer>
    </div>
  );
}
