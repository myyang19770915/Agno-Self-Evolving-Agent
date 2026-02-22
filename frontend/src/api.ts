import axios from 'axios';

const API_BASE_URL = 'http://localhost:7777';

export interface Session {
    session_id: string;
    session_name: string;
    created_at: number;
}

export interface Message {
    id: string;
    role: 'user' | 'ai';
    content: string;
}

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const fetchSessions = async (): Promise<Session[]> => {
    try {
        const response = await api.get('/sessions', {
            params: { limit: 50, sort_order: 'desc' }
        });

        let sessions: Session[] = [];
        // Agno returns { data: [...], meta: {...} }
        if (response.data && response.data.data) {
            sessions = response.data.data;
        } else if (response.data && response.data.items) {
            sessions = response.data.items;
        } else if (Array.isArray(response.data)) {
            sessions = response.data;
        }

        // Ensure sorted by created_at descending (newest first)
        return sessions.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } catch (error) {
        console.error('Error fetching sessions:', error);
        return [];
    }
};

export const createSession = async (): Promise<Session | null> => {
    try {
        const response = await api.post('/sessions', {
            type: 'agent'
        });
        return response.data;
    } catch (error) {
        console.error('Error creating session:', error);
        return null;
    }
};

export const getSessionMessages = async (sessionId: string): Promise<Message[]> => {
    try {
        const response = await api.get(`/sessions/${sessionId}`);
        const sessionData = response.data;
        const messages: Message[] = [];

        // Parse messages from Agno's session detail format (chat_history)
        if (sessionData && sessionData.chat_history && Array.isArray(sessionData.chat_history)) {
            const stateMessages = sessionData.chat_history;
            stateMessages.forEach((msg: any, index: number) => {
                if (msg.role === 'user' || msg.role === 'assistant' || msg.role === 'model') {
                    // Filter out empty messages
                    if (!msg.content) return;

                    messages.push({
                        id: `msg-${index}`,
                        role: (msg.role === 'assistant' || msg.role === 'model') ? 'ai' : 'user',
                        content: typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)
                    });
                }
            });
        }
        return messages;
    } catch (error) {
        console.error(`Error fetching messages for session ${sessionId}:`, error);
        return [];
    }
};

export default api;
