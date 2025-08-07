import dotenv from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";

dotenv.config();

const geminiApiKey = process.env.GEMINI_API_KEY;

if (!geminiApiKey) {
  throw new Error("Error getting Gemini API Key");
}

const genAI = new GoogleGenerativeAI(geminiApiKey);

const gemini_model = genAI.getGenerativeModel({
  model: process.env.GEMINI_API_MODEL,
});

export default gemini_model;
