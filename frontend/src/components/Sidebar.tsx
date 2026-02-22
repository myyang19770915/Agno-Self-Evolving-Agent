import React from 'react';
import { ChevronsUpDown, MessageSquarePlus, MessageSquare } from 'lucide-react';
import type { Session } from '../api';

interface SidebarProps {
    sessions: Session[];
    currentSessionId: string | null;
    onSelectSession: (id: string) => void;
    onNewChat: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ sessions, currentSessionId, onSelectSession, onNewChat }) => {
    return (
        <aside className="w-64 h-full bg-sidebar border-r border-sidebar-border flex flex-col p-2 space-y-4 shrink-0 overflow-y-auto">
            {/* Sidebar Header */}
            <div className="flex items-center justify-between p-2 rounded-md hover:bg-sidebar-accent cursor-pointer transition-colors">
                <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded bg-primary flex items-center justify-center text-primary-foreground font-bold">
                        AG
                    </div>
                    <span className="font-semibold text-sm">Self-Evolving Agent</span>
                </div>
                <ChevronsUpDown className="w-4 h-4 text-muted-foreground" />
            </div>

            {/* New Chat Button */}
            <div className="px-2">
                <button
                    onClick={onNewChat}
                    className="w-full flex items-center justify-center space-x-2 bg-primary text-primary-foreground hover:opacity-90 transition-opacity py-2 rounded-md font-medium text-sm"
                >
                    <MessageSquarePlus className="w-4 h-4" />
                    <span>New Chat</span>
                </button>
            </div>

            {/* Sidebar Content (Session List) */}
            <div className="flex-1 px-2 space-y-1 overflow-y-auto w-full">
                <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 mt-4 px-2">
                    History
                </div>
                {sessions.map(session => {
                    // Handle ISO format vs Unix timestamps from different Agno DB configurations
                    let dateStr = '';
                    if (typeof session.created_at === 'string') {
                        dateStr = new Date(session.created_at).toLocaleString('zh-TW', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
                    } else if (typeof session.created_at === 'number') {
                        dateStr = new Date(session.created_at * 1000).toLocaleString('zh-TW', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
                    }

                    return (
                        <button
                            key={session.session_id}
                            onClick={() => onSelectSession(session.session_id)}
                            className={`w-full flex-col items-start p-2 rounded-md text-left transition-colors ${currentSessionId === session.session_id
                                ? 'bg-sidebar-accent text-sidebar-foreground'
                                : 'hover:bg-sidebar-accent text-muted-foreground hover:text-sidebar-foreground'
                                }`}
                        >
                            <div className="flex items-center space-x-2 w-full">
                                <MessageSquare className="w-4 h-4 shrink-0 text-primary/70" />
                                <span className="font-medium text-sm truncate flex-1">
                                    {session.session_name || '新對話'}
                                </span>
                            </div>
                            <div className="text-[10px] text-muted-foreground/60 w-full text-right mt-1 pr-1 truncate">
                                {dateStr}
                            </div>
                        </button>
                    );
                })}
            </div>

            {/* Sidebar Footer */}
            <div className="p-2 mt-auto">
                <div className="flex items-center justify-between p-2 rounded-md hover:bg-sidebar-accent cursor-pointer transition-colors">
                    <div className="flex items-center space-x-2">
                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs">
                            U
                        </div>
                        <span className="font-medium text-sm">User</span>
                    </div>
                    <ChevronsUpDown className="w-4 h-4 text-muted-foreground" />
                </div>
            </div>
        </aside >
    );
};

export default Sidebar;
