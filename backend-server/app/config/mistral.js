// config/mistral.js
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const mistralApiKey = process.env.MISTRAL_API_KEY;

if (!mistralApiKey) {
  throw new Error("Mistral API key not found in .env");
}

const mistral_model = axios.create({
  baseURL: "https://api.mistral.ai/v1",
  headers: {
    Authorization: `Bearer ${mistralApiKey}`,
    "Content-Type": "application/json",
  },
});

export default mistral_model;