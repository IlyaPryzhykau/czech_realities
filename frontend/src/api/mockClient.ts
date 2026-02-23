import type { ApiClient } from './client';
import type { GameMode, Question, Topic } from '../types';

const topics: Topic[] = [
  {
    id: 'history',
    title: 'History & Culture',
    description: 'Legends, events, and people that shaped Czechia.',
    icon: '🏰',
    color: '#8b5cf6',
  },
  {
    id: 'cities',
    title: 'Cities & Places',
    description: 'From Prague streets to hidden Moravian gems.',
    icon: '🌆',
    color: '#06b6d4',
  },
  {
    id: 'food',
    title: 'Cuisine',
    description: 'Traditional dishes, drinks, and local favorites.',
    icon: '🥨',
    color: '#f97316',
  },
  {
    id: 'nature',
    title: 'Nature',
    description: 'Mountains, forests, rivers, and national parks.',
    icon: '🌲',
    color: '#22c55e',
  },
];

const questionBank: Record<string, Omit<Question, 'topicId'>[]> = {
  history: [
    {
      id: 'h-1',
      prompt: 'Which ruler commissioned Charles Bridge in Prague?',
      imageUrl:
        'https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Charles IV' },
        { id: 'b', text: 'Wenceslaus I' },
        { id: 'c', text: 'Rudolf II' },
        { id: 'd', text: 'George of Poděbrady' },
      ],
    },
  ],
  cities: [
    {
      id: 'c-1',
      prompt: 'What river flows through Prague?',
      imageUrl:
        'https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Danube' },
        { id: 'b', text: 'Vltava' },
        { id: 'c', text: 'Elbe' },
        { id: 'd', text: 'Morava' },
      ],
    },
  ],
  food: [
    {
      id: 'f-1',
      prompt: 'Which dish is a traditional Czech beef stew with dumplings?',
      imageUrl:
        'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Svíčková' },
        { id: 'b', text: 'Goulash soup' },
        { id: 'c', text: 'Bramborák' },
        { id: 'd', text: 'Koláč' },
      ],
    },
  ],
  nature: [
    {
      id: 'n-1',
      prompt: 'Which mountain range is along the Czech-Polish border?',
      imageUrl:
        'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Krkonoše' },
        { id: 'b', text: 'Tatras' },
        { id: 'c', text: 'Alps' },
        { id: 'd', text: 'Šumava' },
      ],
    },
  ],
};

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const mockClient: ApiClient = {
  async getTopics(_mode: GameMode): Promise<Topic[]> {
    await sleep(350);
    return topics;
  },

  async getNextQuestion(topicId: string, _mode: GameMode): Promise<Question> {
    await sleep(400);

    const pool = questionBank[topicId] ?? questionBank.history;
    const item = pool[Math.floor(Math.random() * pool.length)];

    return {
      ...item,
      topicId,
    };
  },
};
