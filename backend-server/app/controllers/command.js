import gemini_model from "../config/gemini.js";
import mistral_model from "../config/mistral.js";
import { gemini_prompt } from "../utils/gemini-prompt.js";
import { mistral_prompt } from "../utils/mistral-prompt.js";
import dotenv from "dotenv";

dotenv.config();

const GeminiResponse = async (req, res) => {
  try {
    const userInput = req.body.input;

    if (!userInput) {
      return res.status(400).json({ success: false, error: "Missing input" });
    }

    const prompt = gemini_prompt(userInput);
    const result = await gemini_model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    res.status(200).json({ success: true, result: text });
  } catch (error) {
    console.error("Gemini API Error:", error.message);
    res.status(500).json({ success: false, error: "Internal Server Error" });
  }
};

const MistralResponse = async (req, res) => {
  try {
    const userInput = req.body.input;

    if (!userInput) {
      return res.status(400).json({ success: false, error: "Missing input" });
    }

    const response = await mistral_model.post("/chat/completions", {
      model: process.env.MISTRAL_API_MODEL,
      messages: [
        {
          role: "system",
          content: mistral_prompt.trim(),
        },
        {
          role: "user",
          content: userInput,
        },
      ],
    });

    const text = response.data.choices[0].message.content;

    res.status(200).json({ success: true, result: text });
  } catch (error) {
    console.error("Mistral API Error:", error.message);
    res.status(500).json({ success: false, error: "Internal Server Error" });
  }
};

export default { GeminiResponse, MistralResponse };
