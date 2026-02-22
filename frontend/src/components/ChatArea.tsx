import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Send, Upload, Square, ChevronDown, ChevronRight, Wrench, Database, Table, Code2, Lightbulb, BarChart3 } from 'lucide-react';
import { getSessionMessages, type Message } from '../api';

interface ChatAreaProps {
    model: string;
    sessionId: string | null;
}

/* ──────────────────────────────────────────────
   型別定義：將 AI 回覆拆分成多個「區塊」
   ────────────────────────────────────────────── */

type BlockType = 'tool' | 'plan' | 'sql' | 'result' | 'python' | 'analysis' | 'chart' | 'text';

interface ContentBlock {
    type: BlockType;
    title: string;
    body: string;
    icon: React.ReactNode;
    color: string;        // border-left 色彩
    bgColor: string;      // 背景色
    collapsed?: boolean;   // 初始是否收合
}

/* ──────────────────────────────────────────────
   可收合的內容區塊元件
   ────────────────────────────────────────────── */

const CollapsibleBlock: React.FC<{
    block: ContentBlock;
    children: React.ReactNode;
}> = ({ block, children }) => {
    const [isOpen, setIsOpen] = useState(!block.collapsed);

    return (
        <div
            className="rounded-lg overflow-hidden transition-all duration-200"
            style={{
                borderLeft: `3px solid ${block.color}`,
                backgroundColor: block.bgColor,
            }}
        >
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 w-full px-4 py-2.5 text-left hover:brightness-110 transition-all"
            >
                {isOpen
                    ? <ChevronDown className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                    : <ChevronRight className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                }
                <span className="shrink-0">{block.icon}</span>
                <span className="text-xs font-semibold tracking-wide" style={{ color: block.color }}>
                    {block.title}
                </span>
            </button>
            {isOpen && (
                <div className="px-4 pb-3 text-sm leading-relaxed">
                    {children}
                </div>
            )}
        </div>
    );
};

/* ──────────────────────────────────────────────
   Markdown 渲染器（含語法高亮）
   ────────────────────────────────────────────── */

const MarkdownRenderer: React.FC<{ content: string }> = ({ content }) => (
    <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
            code({ className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                const codeString = String(children).replace(/\n$/, '');
                if (match) {
                    return (
                        <SyntaxHighlighter
                            style={oneDark}
                            language={match[1]}
                            PreTag="div"
                            customStyle={{
                                margin: '0.5rem 0',
                                borderRadius: '0.5rem',
                                fontSize: '0.8rem',
                            }}
                        >
                            {codeString}
                        </SyntaxHighlighter>
                    );
                }
                return (
                    <code className="bg-[#2a2a3a] text-emerald-300 px-1.5 py-0.5 rounded text-xs font-mono" {...props}>
                        {children}
                    </code>
                );
            },
            table({ children }) {
                return (
                    <div className="overflow-x-auto my-4 rounded-lg border border-border">
                        <table className="w-full text-xs text-left border-collapse">{children}</table>
                    </div>
                );
            },
            thead({ children }) {
                return <thead className="bg-muted/80 text-muted-foreground uppercase text-[10px] tracking-wider">{children}</thead>;
            },
            th({ children }) {
                return <th className="px-4 py-3 font-semibold border-b border-border">{children}</th>;
            },
            tbody({ children }) {
                return <tbody className="divide-y divide-border/50 bg-background/50">{children}</tbody>;
            },
            tr({ children }) {
                return <tr className="hover:bg-muted/30 transition-colors">{children}</tr>;
            },
            td({ children }) {
                return <td className="px-4 py-3 whitespace-nowrap">{children}</td>;
            },
            a({ href, children }) {
                return (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary underline hover:brightness-125">
                        {children}
                    </a>
                );
            },
        }}
    >
        {content}
    </ReactMarkdown>
);

/* ──────────────────────────────────────────────
   AI 思考中動畫元件
   ────────────────────────────────────────────── */

const TypingIndicator = () => (
    <div className="flex items-center space-x-1.5 h-6 px-1">
        <div className="w-2 h-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '300ms' }} />
    </div>
);

/* ──────────────────────────────────────────────
   主元件
   ────────────────────────────────────────────── */

const ChatArea: React.FC<ChatAreaProps> = ({ model, sessionId }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const abortControllerRef = useRef<AbortController | null>(null);

    useEffect(() => {
        if (sessionId) {
            loadMessages(sessionId);
        } else {
            setMessages([{ id: 'init', role: 'ai', content: '你好！我是 Self-Evolving Agent。\n\n### 📋 查詢結果\n\n原始資料庫回傳： | year_week | total_sales | |---:|---:| | 2025-48 | 162462.0 | | 2025-49 | 301589.0 |' }]);
        }
    }, [sessionId]);

    const loadMessages = async (id: string) => {
        const history = await getSessionMessages(id);
        if (history.length > 0) {
            setMessages(history);
        } else {
            setMessages([{ id: 'init', role: 'ai', content: '你好！這是新的對話。今天能為您提供什麼協助？' }]);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    /* ── 送出訊息 (Streaming) ── */

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isGenerating || !sessionId) return;

        const userMessage = inputValue;
        setInputValue('');
        setIsGenerating(true);

        const newUserMsgId = Date.now().toString();
        setMessages((prev) => [...prev, { id: newUserMsgId, role: 'user', content: userMessage }]);

        const aiMsgId = (Date.now() + 1).toString();
        setMessages((prev) => [...prev, { id: aiMsgId, role: 'ai', content: '' }]);

        abortControllerRef.current = new AbortController();

        try {
            const formData = new FormData();
            formData.append('message', userMessage);
            formData.append('stream', 'true');
            // 由於直接傳 model 不會被 AgentOS 處理，我們改用不同的被註冊的 Agent ID 來呼叫對應模型
            formData.append('session_id', sessionId);

            const response = await fetch(`http://localhost:7777/agents/self-evolving-agent-${model}/runs`, {
                method: 'POST',
                body: formData,
                signal: abortControllerRef.current.signal,
            });

            if (!response.ok) throw new Error('Network response was not ok');
            if (!response.body) throw new Error('No readable stream');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                if (value) {
                    const chunkString = decoder.decode(value, { stream: true });
                    const lines = chunkString.split('\n');

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.slice(6));

                                // Agno's RunCompleted event contains the fully aggregated message string.
                                // If we don't ignore it, the UI will append the full message to the end of the streamed chunks, causing duplication.
                                if (data.event && ['RunCompleted', 'ModelRequestCompleted', 'RunContentCompleted', 'RunStarted', 'ModelRequestStarted'].includes(data.event)) {
                                    continue;
                                }

                                const text = data.content ?? data.chunk ?? null;
                                if (text !== null) {
                                    setMessages((prev) =>
                                        prev.map((msg) =>
                                            msg.id === aiMsgId
                                                ? { ...msg, content: msg.content + text }
                                                : msg
                                        )
                                    );
                                }
                            } catch {
                                // 不完整的 JSON chunk，略過
                            }
                        }
                    }
                }
            }
        } catch (error: unknown) {
            if (error instanceof Error && error.name === 'AbortError') {
                console.log('Request aborted');
            } else {
                console.error('Error fetching chat response:', error);
                setMessages((prev) =>
                    prev.map((msg) =>
                        msg.id === aiMsgId
                            ? { ...msg, content: msg.content + '\n\n**系統錯誤**: 無法取得回應。' }
                            : msg
                    )
                );
            }
        } finally {
            setIsGenerating(false);
            abortControllerRef.current = null;
        }
    };

    const stopGeneration = () => {
        abortControllerRef.current?.abort();
    };

    /* ────────────────────────────────────────────
       內容解析：把 raw markdown 拆成結構化區塊
       ──────────────────────────────────────────── */

    const parseContentBlocks = (content: string): ContentBlock[] => {
        const blocks: ContentBlock[] = [];

        // 0. 修復單行 Markdown 格式表格 (例如複製貼上或 LLM 生成少換行的狀況)
        // 將相鄰的 pipe (| |) 中間自動加上換行符號
        let cleanContent = content.replace(/\|\s+\|/g, '|\n|');

        // 1. 擷取工具呼叫紀錄 (tool logs)
        const toolPattern = /([a-zA-Z_][a-zA-Z0-9_]*)\(([^)]*)\)\s*completed in\s*(\d+\.\d+)s\.?/g;
        const toolCalls: { name: string; args: string; time: string }[] = [];
        cleanContent = cleanContent.replace(toolPattern, (_m, name, args, time) => {
            toolCalls.push({ name, args, time });
            return '';
        });

        if (toolCalls.length > 0) {
            const toolBody = toolCalls
                .map((t) => `\`${t.name}(${t.args.length > 60 ? t.args.slice(0, 60) + '…' : t.args})\` — **${t.time}s**`)
                .join('\n');
            blocks.push({
                type: 'tool',
                title: `工具呼叫紀錄 (${toolCalls.length})`,
                body: toolBody,
                icon: <Wrench className="w-3.5 h-3.5" />,
                color: '#64748b',
                bgColor: 'rgba(100,116,139,0.08)',
                collapsed: true,
            });
        }

        // 2. 擷取 chart URLs (去重)
        const chartUrlRegex = /https?:\/\/localhost:7777\/charts\/[a-zA-Z0-9_-]+\.html/g;
        const allChartUrls = cleanContent.match(chartUrlRegex) || [];
        const uniqueChartUrls = [...new Set(allChartUrls)];
        // 從 markdown 文字中移除 chart URL，避免重複顯示
        cleanContent = cleanContent.replace(chartUrlRegex, '').trim();

        // 3. 按照分類標題拆分區塊
        const sectionRegex = /(?:^|\n)#{1,3}\s*(🛠️\s*執行計畫|📊\s*SQL\s*查詢|📋\s*查詢結果|🐍\s*Python\s*程式碼|💡\s*分析與回答|💡\s*分析與建議)[^\n]*/gi;
        const sectionMatches = [...cleanContent.matchAll(sectionRegex)];

        if (sectionMatches.length > 0) {
            // 在第一個區塊之前可能還有純文字
            const beforeFirst = cleanContent.slice(0, sectionMatches[0].index).trim();
            if (beforeFirst) {
                blocks.push({
                    type: 'text',
                    title: '回覆',
                    body: beforeFirst,
                    icon: <Lightbulb className="w-3.5 h-3.5" />,
                    color: '#a78bfa',
                    bgColor: 'rgba(167,139,250,0.06)',
                });
            }

            for (let i = 0; i < sectionMatches.length; i++) {
                const match = sectionMatches[i];
                const header = match[0].trim();
                const startIdx = (match.index ?? 0) + match[0].length;
                const endIdx = i + 1 < sectionMatches.length ? sectionMatches[i + 1].index : cleanContent.length;
                const body = cleanContent.slice(startIdx, endIdx).trim();
                const headerText = match[1] || header;

                if (headerText.includes('執行計畫')) {
                    blocks.push({
                        type: 'plan',
                        title: '執行計畫',
                        body,
                        icon: <Wrench className="w-3.5 h-3.5" />,
                        color: '#38bdf8',
                        bgColor: 'rgba(56,189,248,0.06)',
                    });
                } else if (headerText.includes('SQL')) {
                    blocks.push({
                        type: 'sql',
                        title: 'SQL 查詢',
                        body,
                        icon: <Database className="w-3.5 h-3.5" />,
                        color: '#f59e0b',
                        bgColor: 'rgba(245,158,11,0.06)',
                    });
                } else if (headerText.includes('查詢結果')) {
                    blocks.push({
                        type: 'result',
                        title: '查詢結果',
                        body,
                        icon: <Table className="w-3.5 h-3.5" />,
                        color: '#34d399',
                        bgColor: 'rgba(52,211,153,0.06)',
                    });
                } else if (headerText.includes('Python')) {
                    blocks.push({
                        type: 'python',
                        title: 'Python 程式碼',
                        body,
                        icon: <Code2 className="w-3.5 h-3.5" />,
                        color: '#818cf8',
                        bgColor: 'rgba(129,140,248,0.06)',
                    });
                } else if (headerText.includes('分析')) {
                    blocks.push({
                        type: 'analysis',
                        title: '分析與回答',
                        body,
                        icon: <Lightbulb className="w-3.5 h-3.5" />,
                        color: '#fb923c',
                        bgColor: 'rgba(251,146,60,0.06)',
                    });
                } else {
                    blocks.push({
                        type: 'text',
                        title: headerText.replace(/^#+\s*/, ''),
                        body,
                        icon: <Lightbulb className="w-3.5 h-3.5" />,
                        color: '#a78bfa',
                        bgColor: 'rgba(167,139,250,0.06)',
                    });
                }
            }
        } else {
            // 沒有分類標題：整段作為純文字
            if (cleanContent.trim()) {
                blocks.push({
                    type: 'text',
                    title: '回覆',
                    body: cleanContent.trim(),
                    icon: <Lightbulb className="w-3.5 h-3.5" />,
                    color: '#a78bfa',
                    bgColor: 'rgba(167,139,250,0.06)',
                });
            }
        }

        // 4. 圖表區塊 (去重後的)
        if (uniqueChartUrls.length > 0) {
            blocks.push({
                type: 'chart',
                title: `互動式圖表 (${uniqueChartUrls.length})`,
                body: uniqueChartUrls.join('\n'),
                icon: <BarChart3 className="w-3.5 h-3.5" />,
                color: '#22d3ee',
                bgColor: 'rgba(34,211,238,0.06)',
            });
        }

        return blocks;
    };

    /* ────────────────────────────────────────────
       渲染 AI 訊息
       ──────────────────────────────────────────── */

    const renderAIMessage = (content: string) => {
        const blocks = parseContentBlocks(content);

        if (blocks.length === 0) {
            return (
                <div className="prose prose-invert max-w-none text-sm leading-relaxed">
                    <MarkdownRenderer content={content} />
                </div>
            );
        }

        return (
            <div className="space-y-2.5 w-full">
                {blocks.map((block, idx) => {
                    if (block.type === 'chart') {
                        const urls = block.body.split('\n').filter(Boolean);
                        return (
                            <CollapsibleBlock key={idx} block={block}>
                                {urls.map((url, ci) => (
                                    <div key={ci} className="mt-1 rounded-lg overflow-hidden border border-border w-full h-[420px] bg-[#1a1a2e]">
                                        <iframe src={url} className="w-full h-full border-none" title={`Chart ${ci}`} />
                                    </div>
                                ))}
                            </CollapsibleBlock>
                        );
                    }

                    if (block.type === 'tool') {
                        return (
                            <CollapsibleBlock key={idx} block={block}>
                                <div className="space-y-1">
                                    <MarkdownRenderer content={block.body} />
                                </div>
                            </CollapsibleBlock>
                        );
                    }

                    return (
                        <CollapsibleBlock key={idx} block={block}>
                            <MarkdownRenderer content={block.body} />
                        </CollapsibleBlock>
                    );
                })}
            </div>
        );
    };

    /* ── JSX 主渲染 ── */

    return (
        <div className="flex-1 flex flex-col h-full bg-background relative px-4 pb-2">
            {/* 訊息列表 */}
            <div className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
                <div className="max-w-4xl mx-auto space-y-6">
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`rounded-2xl px-5 py-3 ${msg.role === 'user'
                                    ? 'max-w-[75%] bg-primary text-primary-foreground rounded-tr-sm'
                                    : 'max-w-[90%] w-full bg-muted/40 text-foreground rounded-tl-sm border border-border/40'
                                    }`}
                            >
                                {msg.role === 'user'
                                    ? <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                                    : (msg.content === '' && isGenerating)
                                        ? <TypingIndicator />
                                        : renderAIMessage(msg.content)
                                }
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} className="h-4" />
                </div>
            </div>

            {/* 輸入區 */}
            <div className="w-full max-w-4xl mx-auto pb-6 px-4 pt-2">
                <div className="relative flex flex-col bg-muted/60 border border-border rounded-2xl shadow-sm focus-within:ring-1 focus-within:ring-primary focus-within:border-primary transition-all">
                    <textarea
                        className="w-full bg-transparent resize-none outline-none max-h-48 min-h-[60px] py-4 px-4 text-sm text-foreground placeholder-muted-foreground"
                        placeholder="請輸入訊息或指令..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSendMessage();
                            }
                        }}
                    />
                    <div className="flex items-center justify-between px-3 pb-3">
                        <div className="flex space-x-2">
                            <button
                                className="p-2 text-muted-foreground hover:bg-muted rounded-full transition-colors focus:outline-none"
                                title="Upload file (Coming Soon)"
                            >
                                <Upload className="w-4 h-4" />
                            </button>
                        </div>

                        {isGenerating ? (
                            <button
                                onClick={stopGeneration}
                                className="p-2 bg-destructive text-destructive-foreground hover:bg-destructive/90 rounded-full transition-colors flex items-center justify-center focus:outline-none shadow-sm"
                            >
                                <Square className="w-4 h-4 fill-current" />
                            </button>
                        ) : (
                            <button
                                onClick={handleSendMessage}
                                disabled={!inputValue.trim() || !sessionId}
                                className="p-2 bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed rounded-full transition-colors flex items-center justify-center focus:outline-none shadow-sm"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        )}
                    </div>
                </div>
                <div className="text-center mt-3">
                    <span className="text-xs text-muted-foreground font-medium flex items-center justify-center space-x-1">
                        <span>AI 可能產生不準確的資訊，請自行驗證重要內容。</span>
                    </span>
                </div>
            </div>
        </div>
    );
};

export default ChatArea;
