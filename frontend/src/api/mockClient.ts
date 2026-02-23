import type { ApiClient } from './client';
import type { GameMode, Question, Topic } from '../types';

const topics: Topic[] = [
  {
    id: 'history',
    title: 'Historie a kultura',
    description: 'Legendy, události a osobnosti, které formovaly Česko.',
    icon: '🏰',
    color: '#8b5cf6',
  },
  {
    id: 'cities',
    title: 'Města a místa',
    description: 'Od pražských ulic po skryté moravské poklady.',
    icon: '🌆',
    color: '#06b6d4',
  },
  {
    id: 'food',
    title: 'Kuchyně',
    description: 'Tradiční jídla, nápoje a místní oblíbené speciality.',
    icon: '🥨',
    color: '#f97316',
  },
  {
    id: 'nature',
    title: 'Příroda',
    description: 'Hory, lesy, řeky a národní parky.',
    icon: '🌲',
    color: '#22c55e',
  },
];

const questionBank: Record<string, Omit<Question, 'topicId'>[]> = {
  history: [
    {
      id: 'h-1',
      prompt: 'Který panovník nechal postavit Karlův most v Praze?',
      imageUrl:
        'https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Karel IV.' },
        { id: 'b', text: 'Václav I.' },
        { id: 'c', text: 'Rudolf II.' },
        { id: 'd', text: 'Jiří z Poděbrad' },
      ],
    },
  ],
  cities: [
    {
      id: 'c-1',
      prompt: 'Která řeka protéká Prahou?',
      imageUrl:
        'https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Dunaj' },
        { id: 'b', text: 'Vltava' },
        { id: 'c', text: 'Labe' },
        { id: 'd', text: 'Morava' },
      ],
    },
  ],
  food: [
    {
      id: 'f-1',
      prompt: 'Které jídlo je tradiční česká hovězí omáčka s knedlíkem?',
      imageUrl:
        'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80',
      options: [
        { id: 'a', text: 'Svíčková' },
        { id: 'b', text: 'Gulášová polévka' },
        { id: 'c', text: 'Bramborák' },
        { id: 'd', text: 'Koláč' },
      ],
    },
  ],
  nature: [
    {
      id: 'n-1',
      prompt: 'Které pohoří leží na česko-polské hranici?',
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
