import React from 'react';
import { Settings, Share, AlignLeft } from 'lucide-react';

interface TopBarProps {
    model: string;
    setModel: (model: string) => void;
}

const TopBar: React.FC<TopBarProps> = ({ model, setModel }) => {
    return (
        <header className="h-16 border-b border-border flex items-center justify-between px-6 shrink-0 bg-background/95 backdrop-blur z-10 sticky top-0 w-full">
            <div className="flex items-center space-x-4">
                {/* Mobile menu toggle could go here */}
                <button className="lg:hidden p-2 -ml-2 text-muted-foreground hover:text-foreground">
                    <AlignLeft className="w-5 h-5" />
                </button>

                <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-muted-foreground">Model:</span>
                    <select
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        className="bg-transparent border border-muted rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary cursor-pointer hover:bg-muted/50 transition-colors"
                    >
                        <option className="bg-background" value="gpt-5-mini">gpt-5-mini</option>
                        <option className="bg-background" value="deepseek-reasoner">deepseek-reasoner</option>
                        <option className="bg-background" value="deepseek-chat">deepseek-chat</option>
                    </select>
                </div>
            </div>

            <div className="flex items-center space-x-3">
                <button className="p-2 text-muted-foreground hover:bg-muted/50 rounded-md transition-colors" title="Settings">
                    <Settings className="w-5 h-5" />
                </button>
                <button className="p-2 text-muted-foreground hover:bg-muted/50 rounded-md transition-colors" title="Share Chat">
                    <Share className="w-5 h-5" />
                </button>
            </div>
        </header>
    );
};

export default TopBar;
