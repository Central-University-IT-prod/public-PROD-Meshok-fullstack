import type { UserLevel } from "./level";

export interface Client {
	age: number;
	id: number;
	email: string;
	gender: "Male" | "Female";
	level: UserLevel;
}