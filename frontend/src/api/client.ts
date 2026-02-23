import type { Question, Topic } from '../types';

export interface ApiClient {
  getTopics(): Promise<Topic[]>;
  getQuestionsByTopic(topicId: string): Promise<Question[]>;
  getRandomQuestion(): Promise<Question>;
  getRandomTicket(): Promise<Question[]>;
}

export const createApiClient = (impl: ApiClient): ApiClient => impl;
