import type { GameMode, Question, Topic } from '../types';

export interface ApiClient {
  getTopics(mode: GameMode): Promise<Topic[]>;
  getNextQuestion(topicId: string, mode: GameMode): Promise<Question>;
}

export const createApiClient = (impl: ApiClient): ApiClient => impl;
