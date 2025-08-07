import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import CommandRoute from "./app/routes/command.js";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use("/api/command/", CommandRoute);

app.get("/", (req, res) => {
  res.json({ message: "Server is Running" });
});

app.listen(PORT, () => {
  console.log("Server is Running");
});
