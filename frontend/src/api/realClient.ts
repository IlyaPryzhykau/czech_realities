import type { ApiClient } from './client';
import type { Question, QuestionOption, Topic } from '../types';

type AnyRecord = Record<string, unknown>;

const DEFAULT_API_BASE_URL = '';
const RAW_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL) as string;
const API_BASE_URL = RAW_BASE_URL.replace(/\/$/, '');

const TOPIC_ICONS = ['🏰', '🌆', '🌲', '🥨', '🏛️', '🎭', '🗺️', '📚'];
const TOPIC_COLORS = ['#8b5cf6', '#06b6d4', '#22c55e', '#f97316', '#ef4444', '#3b82f6', '#14b8a6', '#a855f7'];

const getNumber = (value: unknown): number | null => {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string' && value.trim() !== '' && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return null;
};

const getText = (value: unknown): string => (typeof value === 'string' ? value : '');

const toAbsoluteUrl = (value: string): string => {
  if (!value) return '';
  if (/^https?:\/\//i.test(value)) return value;
  return `${API_BASE_URL}${value.startsWith('/') ? '' : '/'}${value}`;
};

const extractImageUrl = (source: AnyRecord): string | undefined => {
  const raw =
    getText(source.image_url) ||
    getText(source.imageUrl) ||
    getText(source.image_path) ||
    getText(source.imagePath) ||
    getText(source.image);

  if (!raw) return undefined;
  return toAbsoluteUrl(raw);
};

const mapTopic = (rawTopic: unknown, index = 0): Topic => {
  const item = (rawTopic ?? {}) as AnyRecord;
  const id = String(getNumber(item.id) ?? item.id ?? `topic-${index + 1}`);
  const title = getText(item.name) || `Téma ${id}`;

  return {
    id,
    title,
    description: `Procvičování tématu: ${title}`,
    icon: TOPIC_ICONS[index % TOPIC_ICONS.length],
    color: TOPIC_COLORS[index % TOPIC_COLORS.length],
  };
};

const mapAnswer = (rawAnswer: unknown, index = 0): QuestionOption => {
  const item = (rawAnswer ?? {}) as AnyRecord;
  const isCorrect =
    typeof item.is_correct === 'boolean'
      ? item.is_correct
      : typeof item.correct === 'boolean'
        ? item.correct
        : undefined;

  const imageUrl = extractImageUrl(item);
  const text = getText(item.text) || getText(item.name);

  return {
    id: String(getNumber(item.id) ?? item.id ?? `opt-${index + 1}`),
    text: text || (imageUrl ? '' : `Varianta ${index + 1}`),
    imageUrl,
    isCorrect,
    correct: isCorrect,
  };
};

const mapQuestion = (rawQuestion: unknown): Question => {
  const item = (rawQuestion ?? {}) as AnyRecord;
  const topic = (item.topic ?? {}) as AnyRecord;
  const mappedTopicId = getNumber(topic.id) ?? getNumber(item.topic_id) ?? item.topic_id ?? 'unknown';

  const rawAnswers = Array.isArray(item.answers) ? item.answers : [];

  return {
    id: String(getNumber(item.id) ?? item.id ?? crypto.randomUUID()),
    topicId: String(mappedTopicId),
    prompt: getText(item.text) || 'Otázka bez textu',
    imageUrl: extractImageUrl(item),
    options: rawAnswers.map(mapAnswer),
  };
};

const request = async <T>(path: string): Promise<T> => {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return (await response.json()) as T;
};

export const realApiClient: ApiClient = {
  async getTopics(): Promise<Topic[]> {
    const data = await request<unknown[]>('/topic/');
    return data.map(mapTopic);
  },

  async getQuestionsByTopic(topicId: string): Promise<Question[]> {
    const data = await request<unknown[]>(`/question/by-topic/${topicId}`);
    return data.map(mapQuestion);
  },

  async getRandomQuestion(): Promise<Question> {
    const data = await request<unknown>('/question/random-one');
    return mapQuestion(data);
  },

  async getRandomTicket(): Promise<Question[]> {
    const data = await request<unknown[]>('/question/random-ticket');
    return data.map(mapQuestion);
  },
};
