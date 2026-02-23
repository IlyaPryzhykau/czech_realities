import { useEffect, useMemo, useState, type CSSProperties } from 'react';
import './App.css';
import { createApiClient } from './api/client';
import { mockClient } from './api/mockClient';
import type { GameMode, Question, Topic } from './types';

type View = 'landing' | 'topics' | 'question';

const api = createApiClient(mockClient);

const modeMeta: Record<GameMode, { title: string; description: string; badge: string }> = {
  classic: {
    title: 'Classic',
    description: 'No rush, just thoughtful exploration and learning.',
    badge: 'Balanced',
  },
  timed: {
    title: 'Blitz',
    description: 'Answer fast and keep the momentum high.',
    badge: 'Fast-paced',
  },
  debate: {
    title: 'Debate',
    description: 'Pick a side and discuss with your group.',
    badge: 'Social',
  },
};

function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    const fromStorage = localStorage.getItem('theme');
    return fromStorage === 'light' ? 'light' : 'dark';
  });
  const [view, setView] = useState<View>('landing');
  const [mode, setMode] = useState<GameMode>('classic');
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem('theme', theme);
  }, [theme]);

  const headerSubtitle = useMemo(() => {
    if (view === 'landing') return 'Discover Czech realities in a polished, playful format.';
    if (view === 'topics') return `Mode: ${modeMeta[mode].title}`;
    return selectedTopic ? `Topic: ${selectedTopic.title}` : 'Question time';
  }, [view, mode, selectedTopic]);

  const startMode = async (nextMode: GameMode) => {
    setMode(nextMode);
    setIsLoading(true);
    setView('topics');
    try {
      const data = await api.getTopics(nextMode);
      setTopics(data);
    } finally {
      setIsLoading(false);
    }
  };

  const pickTopic = async (topic: Topic) => {
    setSelectedTopic(topic);
    setSelectedOption(null);
    setIsLoading(true);
    setView('question');
    try {
      const next = await api.getNextQuestion(topic.id, mode);
      setQuestion(next);
    } finally {
      setIsLoading(false);
    }
  };

  const nextQuestion = async () => {
    if (!selectedTopic) return;
    setSelectedOption(null);
    setIsLoading(true);
    try {
      const next = await api.getNextQuestion(selectedTopic.id, mode);
      setQuestion(next);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />
      <div className="bg-orb orb-3" />

      <main className="container">
        <header className="topbar glass">
          <div>
            <h1>Czech Realities</h1>
            <p>{headerSubtitle}</p>
          </div>
          <button
            className="theme-toggle"
            onClick={() => setTheme((v) => (v === 'dark' ? 'light' : 'dark'))}
            type="button"
          >
            {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
          </button>
        </header>

        {view === 'landing' && (
          <section className="mode-grid">
            {(Object.keys(modeMeta) as GameMode[]).map((modeKey) => (
              <article className="mode-card glass" key={modeKey}>
                <span className="badge">{modeMeta[modeKey].badge}</span>
                <h2>{modeMeta[modeKey].title}</h2>
                <p>{modeMeta[modeKey].description}</p>
                <button onClick={() => void startMode(modeKey)} type="button">
                  Start mode
                </button>
              </article>
            ))}
          </section>
        )}

        {view === 'topics' && (
          <section className="glass panel">
            <div className="panel-head">
              <h2>Choose your topic</h2>
              <button className="ghost" onClick={() => setView('landing')} type="button">
                ← Back
              </button>
            </div>
            {isLoading ? (
              <p className="muted">Loading topics…</p>
            ) : (
              <div className="topic-grid">
                {topics.map((topic) => (
                  <button
                    key={topic.id}
                    className="topic-card"
                    style={{ '--topic-color': topic.color } as CSSProperties}
                    onClick={() => void pickTopic(topic)}
                    type="button"
                  >
                    <span className="topic-icon">{topic.icon}</span>
                    <div>
                      <strong>{topic.title}</strong>
                      <p>{topic.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </section>
        )}

        {view === 'question' && (
          <section className="glass panel question-panel">
            <div className="panel-head">
              <h2>{question?.prompt ?? 'Loading question…'}</h2>
              <button className="ghost" onClick={() => setView('topics')} type="button">
                Change topic
              </button>
            </div>

            {question?.imageUrl && <img src={question.imageUrl} alt="Question visual" className="question-image" />}

            <div className="options-grid">
              {(question?.options ?? []).map((opt) => (
                <button
                  key={opt.id}
                  className={`option-btn ${selectedOption === opt.id ? 'selected' : ''}`}
                  onClick={() => setSelectedOption(opt.id)}
                  type="button"
                >
                  {opt.text}
                </button>
              ))}
            </div>

            <div className="actions">
              <button className="ghost" onClick={() => setSelectedOption(null)} type="button">
                Reset
              </button>
              <button onClick={() => void nextQuestion()} disabled={isLoading} type="button">
                {isLoading ? 'Loading…' : 'Next question'}
              </button>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
