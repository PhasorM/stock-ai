import { useState, useRef, useEffect } from 'react';

// Define the shape of a chat message
interface Message {
  sender: 'bot' | 'user';
  text: string;
}

function App() {
  const [isListening, setIsListening] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'bot', text: 'System Online. Neural Link Established.' }
  ]);
  
  const endOfChatRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    endOfChatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (sender: 'bot' | 'user', text: string) => {
    setMessages(prev => [...prev, { sender, text }]);
  };

  // --- THE REAL BACKEND CONNECTION ---
  const toggleMic = async () => {
    // Prevent double-clicking while it's already working
    if (isListening) return;

    setIsListening(true);
    
    try {
      // 1. Call your Python Server
      // Note: This waits for the 5-second recording to finish
      const response = await fetch("http://127.0.0.1:8000/run-agent");
      
      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const data = await response.json();
      
      // 2. Display what you said (User)
      if (data.user_text) {
        addMessage('user', data.user_text);
      } else {
        addMessage('user', "(Silence)");
      }

      // 3. Display what the AI said (Bot)
      if (data.bot_text) {
        addMessage('bot', data.bot_text);
      }

    } catch (error) {
      console.error("Connection failed:", error);
      addMessage('bot', "⚠️ Error: Cannot connect to Python Brain. Is server.py running?");
    } finally {
      setIsListening(false); // Re-enable the button
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      
      {/* MAIN CONTAINER */}
      <div className="w-full max-w-lg bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden relative">
        
        {/* TOP BAR */}
        <div className="bg-slate-800 p-4 border-b border-slate-700 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className={`h-3 w-3 rounded-full ${isListening ? 'bg-red-500 animate-pulse shadow-[0_0_10px_red]' : 'bg-emerald-500'}`}></div>
            <h1 className="text-lg font-bold text-cyan-400 tracking-widest">A.I. VOICE AGENT</h1>
          </div>
          <div className="text-xs text-slate-500 font-mono">LIVE CONNECTION</div>
        </div>

        {/* CHAT HISTORY */}
        <div className="h-[400px] overflow-y-auto p-4 space-y-4 bg-[#0B1120]">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] p-3 text-sm rounded-xl font-mono leading-relaxed ${
                msg.sender === 'user' 
                  ? 'bg-cyan-900/40 text-cyan-100 border border-cyan-700/50 rounded-br-none' 
                  : 'bg-slate-800 text-slate-300 border border-slate-700 rounded-bl-none'
              }`}>
                {msg.sender === 'bot' && <span className="text-xs text-slate-500 block mb-1">🤖 AGENT</span>}
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={endOfChatRef} />
        </div>

        {/* BOTTOM CONTROLS */}
        <div className="bg-slate-800 p-6 border-t border-slate-700 flex justify-center relative">
          
          {/* Visual Waveform Effect */}
          {isListening && (
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent animate-pulse"></div>
          )}

          <button 
            onClick={toggleMic}
            disabled={isListening} // Disable button while recording
            className={`
              h-20 w-20 rounded-full flex items-center justify-center transition-all duration-300 border-4 outline-none
              ${isListening 
                ? 'bg-red-500/10 border-red-500 text-red-500 cursor-wait' 
                : 'bg-slate-700 border-slate-600 text-cyan-400 hover:bg-slate-600 hover:scale-105 hover:border-cyan-400 cursor-pointer'}
            `}
          >
            {/* SVG MIC ICON */}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className={`w-8 h-8 ${isListening ? 'animate-bounce' : ''}`}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 1.5a3 3 0 013 3v4.5a3 3 0 01-6 0v-4.5a3 3 0 013-3z" />
            </svg>
          </button>
        </div>
      </div>

      <p className="mt-4 text-slate-500 text-xs">Connected to Localhost:8000</p>
    </div>
  );
}

export default App;