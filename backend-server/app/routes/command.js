import express from "express";
import CommandController from "../controllers/command.js";

const router = express.Router();

router.post("/gemini", CommandController.GeminiResponse);

router.post("/mistral", CommandController.MistralResponse);

export default router;
