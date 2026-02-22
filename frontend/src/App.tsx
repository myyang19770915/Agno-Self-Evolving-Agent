import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import TopBar from './components/TopBar';
import { fetchSessions, createSession, type Session } from './api';

function App() {
  const [model, setModel] = useState('gpt-5-mini');
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    const data = await fetchSessions();
    setSessions(data);
    if (data.length > 0 && !currentSessionId) {
      setCurrentSessionId(data[0].session_id);
    } else if (data.length === 0) {
      handleNewChat();
    }
  };

  const handleNewChat = async () => {
    const newSession = await createSession();
    if (newSession) {
      setSessions((prev) => [newSession, ...prev]);
      setCurrentSessionId(newSession.session_id);
    }
  };

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={setCurrentSessionId}
        onNewChat={handleNewChat}
      />

      <div className="flex flex-col flex-1 h-full min-w-0 bg-background">
        <TopBar model={model} setModel={setModel} />
        <ChatArea model={model} sessionId={currentSessionId} />
      </div>
    </div>
  );
}

export default App;
