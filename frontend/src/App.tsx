import { useEffect, useMemo, useState, type CSSProperties } from 'react';
import './App.css';
import { createApiClient } from './api/client';
import { mockClient } from './api/mockClient';
import { realApiClient } from './api/realClient';
import type { GameMode, Question, Topic } from './types';

type View = 'landing' | 'topics' | 'question';

const useMock = String(import.meta.env.VITE_USE_MOCK ?? 'true').toLowerCase() !== 'false';
const api = createApiClient(useMock ? mockClient : realApiClient);

const modeMeta: Record<GameMode, { title: string; description: string; badge: string }> = {
  classic: {
    title: 'Klasický',
    description: 'Výběr tématu a procvičování otázek v dané oblasti.',
    badge: 'Podle tématu',
  },
  timed: {
    title: 'Náhodná otázka',
    description: 'Rychlý trénink: aplikace vygeneruje jednu náhodnou otázku.',
    badge: 'random-one',
  },
  debate: {
    title: 'Náhodný testový lístek',
    description: 'Balíček otázek napříč tématy (random-ticket).',
    badge: 'random-ticket',
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
  const [questionQueue, setQuestionQueue] = useState<Question[]>([]);
  const [queueIndex, setQueueIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const question = questionQueue[queueIndex] ?? null;

  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem('theme', theme);
  }, [theme]);

  const headerSubtitle = useMemo(() => {
    if (view === 'landing') return 'Procvičuj české reálie v moderním a přehledném rozhraní.';
    if (view === 'topics') return `Režim: ${modeMeta[mode].title}`;
    return selectedTopic ? `Téma: ${selectedTopic.title}` : `Režim: ${modeMeta[mode].title}`;
  }, [view, mode, selectedTopic]);

  const startMode = async (nextMode: GameMode) => {
    setMode(nextMode);
    setSelectedTopic(null);
    setQuestionQueue([]);
    setQueueIndex(0);
    setSelectedOption(null);
    setError(null);

    if (nextMode === 'classic') {
      setIsLoading(true);
      setView('topics');
      try {
        const data = await api.getTopics();
        setTopics(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Nepodařilo se načíst témata.');
      } finally {
        setIsLoading(false);
      }
      return;
    }

    setView('question');
    setIsLoading(true);
    try {
      if (nextMode === 'timed') {
        const next = await api.getRandomQuestion();
        setQuestionQueue([next]);
        setQueueIndex(0);
      } else {
        const ticket = await api.getRandomTicket();
        setQuestionQueue(ticket);
        setQueueIndex(0);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nepodařilo se načíst otázku.');
    } finally {
      setIsLoading(false);
    }
  };

  const pickTopic = async (topic: Topic) => {
    setSelectedTopic(topic);
    setSelectedOption(null);
    setError(null);
    setIsLoading(true);
    setView('question');
    try {
      const questions = await api.getQuestionsByTopic(topic.id);
      setQuestionQueue(questions);
      setQueueIndex(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nepodařilo se načíst otázky pro téma.');
    } finally {
      setIsLoading(false);
    }
  };

  const nextQuestion = async () => {
    setSelectedOption(null);
    setError(null);

    if (mode !== 'timed' && queueIndex < questionQueue.length - 1) {
      setQueueIndex((prev) => prev + 1);
      return;
    }

    setIsLoading(true);
    try {
      if (mode === 'timed') {
        const next = await api.getRandomQuestion();
        setQuestionQueue([next]);
        setQueueIndex(0);
        return;
      }

      if (mode === 'debate') {
        const ticket = await api.getRandomTicket();
        setQuestionQueue(ticket);
        setQueueIndex(0);
        return;
      }

      if (!selectedTopic) return;
      const questions = await api.getQuestionsByTopic(selectedTopic.id);
      setQuestionQueue(questions);
      setQueueIndex(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nepodařilo se načíst další otázku.');
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
                    <li><strong>Výběr tématu</strong> – endpoint <code>/question/by-topic/{'{id}'}</code>.</li>
                    <li><strong>Náhodná otázka</strong> – endpoint <code>/question/random-one</code>.</li>
                    <li><strong>Náhodný testový lístek</strong> – endpoint <code>/question/random-ticket</code>.</li>
                  </ul>
                </div>
                <div>
                  <h3>Data source</h3>
                  <ul>
                    <li>Aktivní client: <strong>{useMock ? 'mockClient' : 'realApiClient'}</strong>.</li>
                    <li>Pro produkci nastav <code>VITE_USE_MOCK=false</code>.</li>
                    <li>Base URL: <code>{String(import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')}</code>.</li>
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
              <h2>{question?.prompt ?? (isLoading ? 'Načítám otázku…' : 'Otázka není dostupná')}</h2>
              <button
                className="ghost"
                onClick={() => setView(mode === 'classic' ? 'topics' : 'landing')}
                type="button"
              >
                {mode === 'classic' ? 'Změnit téma' : '← Zpět'}
              </button>
            </div>

            {error && <p className="muted">⚠️ {error}</p>}

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
