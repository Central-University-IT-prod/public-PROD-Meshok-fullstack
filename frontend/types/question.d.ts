export type QuestionType = "Smile" | "Range"

export interface Question {
	type: QuestionType;
	description: string;
	category?: string;
	id: number;
}