import { useEffect, useMemo, useState, type CSSProperties } from 'react';
import './App.css';
import { createApiClient } from './api/client';
import { mockClient } from './api/mockClient';
import type { GameMode, Question, Topic } from './types';

type View = 'landing' | 'topics' | 'question';

const api = createApiClient(mockClient);

const modeMeta: Record<GameMode, { title: string; description: string; badge: string }> = {
  classic: {
    title: 'Klasický',
    description: 'Bez stresu – promyšlené procvičování a učení.',
    badge: 'Vyvážený',
  },
  timed: {
    title: 'Rychlý',
    description: 'Odpovídej rychle a drž tempo.',
    badge: 'Na čas',
  },
  debate: {
    title: 'Diskuze',
    description: 'Vyber si stranu a diskutuj se skupinou.',
    badge: 'Společenský',
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
    if (view === 'landing') return 'Procvičuj české reálie v moderním a přehledném rozhraní.';
    if (view === 'topics') return `Režim: ${modeMeta[mode].title}`;
    return selectedTopic ? `Téma: ${selectedTopic.title}` : 'Otázka';
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
            <h1>České reálie</h1>
            <p>{headerSubtitle}</p>
          </div>
          <button
            className="theme-toggle"
            onClick={() => setTheme((v) => (v === 'dark' ? 'light' : 'dark'))}
            type="button"
          >
            {theme === 'dark' ? '☀️ Světlý' : '🌙 Tmavý'}
          </button>
        </header>

        {view === 'landing' && (
          <>
            <section className="glass panel intro-panel">
              <h2>Databanka testových úloh z českých reálií</h2>
              <p>Vítej! Tento trénink je určen pro přípravu na zkoušku z českých reálií.</p>

              <div className="intro-grid">
                <div>
                  <h3>Co najdeš v aplikaci</h3>
                  <ul>
                    <li><strong>Výběr tématu</strong> – procvičování v konkrétní oblasti.</li>
                    <li><strong>Náhodná otázka</strong> – rychlé ověření znalostí.</li>
                    <li><strong>Náhodný testový lístek</strong> – mix otázek napříč tématy.</li>
                  </ul>
                </div>
                <div>
                  <h3>Jak funguje otázka</h3>
                  <ul>
                    <li>Každá otázka má zadání a možnosti odpovědí.</li>
                    <li>Správná je vždy jen jedna odpověď.</li>
                    <li>Zadání může obsahovat text i obrázek.</li>
                  </ul>
                </div>
              </div>
            </section>

            <section className="mode-grid">
              {(Object.keys(modeMeta) as GameMode[]).map((modeKey) => (
                <article className="mode-card glass" key={modeKey}>
                  <span className="badge">{modeMeta[modeKey].badge}</span>
                  <h2>{modeMeta[modeKey].title}</h2>
                  <p>{modeMeta[modeKey].description}</p>
                  <button onClick={() => void startMode(modeKey)} type="button">
                    Spustit režim
                  </button>
                </article>
              ))}
            </section>
          </>
        )}

        {view === 'topics' && (
          <section className="glass panel">
            <div className="panel-head">
              <h2>Vyber téma</h2>
              <button className="ghost" onClick={() => setView('landing')} type="button">
                ← Zpět
              </button>
            </div>
            {isLoading ? (
              <p className="muted">Načítám témata…</p>
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
              <h2>{question?.prompt ?? 'Načítám otázku…'}</h2>
              <button className="ghost" onClick={() => setView('topics')} type="button">
                Změnit téma
              </button>
            </div>

            {question?.imageUrl && <img src={question.imageUrl} alt="Ilustrace otázky" className="question-image" />}

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
                {isLoading ? 'Načítám…' : 'Další otázka'}
              </button>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
