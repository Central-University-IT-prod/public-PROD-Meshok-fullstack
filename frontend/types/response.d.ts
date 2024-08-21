import type { Question } from "./question";
import type { Client } from "./client";
export interface Response {
	answer: number;
	answer_id: number;
	user: Client;
	question: Question
}