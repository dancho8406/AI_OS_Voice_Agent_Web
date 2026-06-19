import React, { useState, useEffect } from 'react';

interface ChatMessage {
  sender: 'user' | 'ai';
  text: string; // Поправено от str на string за TypeScript
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isListening, setIsListening] = useState(false);
  const [browserSupported, setBrowserSupported] = useState(true);
  
  // Проверяваме дали браузърът (на телефона или PC) поддържа уеб гласово разпознаване
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
  
  useEffect(() => {
    if (!SpeechRecognition) {
      setBrowserSupported(false);
    }
  }, []);
  
  const handleVoiceCommand = () => {
    if (!SpeechRecognition) return;
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'bg-BG'; // Настройваме да слуша на български език
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    
    recognition.onresult = async (event: any) => {
      const textCommand = event.results[0][0].transcript;
      
      // 1. Добавяме гласа на потребителя в чата
      setMessages(prev => [...prev, { sender: 'user', text: textCommand }]);
      
      try {
        // Директна и сигурна връзка към реалния ти сървър в Google Cloud Run
        const response = await fetch('https://web-agent-896874138272.europe-west4.run.app/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: textCommand })
        });
        
        const data = await response.json();
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        
        // 2. Проверяваме какво е решил ИИ в Облака
        if (parsedData.action === 'open_url') {
          setMessages(prev => [...prev, { sender: 'ai', text: `🌐 Отварям: ${parsedData.url}` }]);
          
          // Критичен момент за Уеб: Браузърът на устройството (PC/Телефон) сам отваря сайта!
          window.open(parsedData.url, '_blank');
        } else if (parsedData.action === 'chat') {
          setMessages(prev => [...prev, { sender: 'ai', text: parsedData.reply }]);
        }
      
      } catch (error) {
        setMessages(prev => [...prev, { sender: 'ai', text: '❌ Грешка при връзка с уеб сървъра.' }]);
      }
    };
    
    recognition.start();
  };
  
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#0070f3' }}>🌐 AI OS Voice Agent - Web</h1>
      
      {!browserSupported && (
        <p style={{ color: 'red', textAlign: 'center' }}>⚠️ Вашият браузър не поддържа гласово разпознаване.</p>
      )}
      
      <div style={{ border: '1px solid #ccc', borderRadius: '8px', height: '300px', overflowY: 'auto', padding: '10px', marginBottom: '20px', background: '#f9f9f9' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: '5px 0' }}>
            <span style={{ background: msg.sender === 'user' ? '#0070f3' : '#e1e1e1', color: msg.sender === 'user' ? '#fff' : '#000', padding: '6px 12px', borderRadius: '12px', display: 'inline-block' }}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      
      <div style={{ textAlign: 'center' }}>
        <button 
          onClick={handleVoiceCommand}
          disabled={!browserSupported || isListening}
          style={{ padding: '15px 30px', fontSize: '18px', borderRadius: '50px', border: 'none', background: isListening ? '#ff4d4d' : '#0070f3', color: '#fff', cursor: 'pointer', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
        >
          {isListening ? '🎙️ Слушам...' : '🎤 Натисни и Говори'}
        </button>
      </div>
    </div>
  );
}
