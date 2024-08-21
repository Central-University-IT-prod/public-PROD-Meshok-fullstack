import type { QuestionType } from "./question";

export interface Metric {
	question: string;
	type: QuestionType;
	stats: Record<string, number>;
}