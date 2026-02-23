export type GameMode = 'classic' | 'timed' | 'debate';

export interface Topic {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
}

export interface QuestionOption {
  id: string;
  text: string;
  isCorrect?: boolean;
}

export interface Question {
  id: string;
  topicId: string;
  prompt: string;
  imageUrl?: string;
  options: QuestionOption[];
}
