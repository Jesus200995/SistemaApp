import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { PrismaClient } from "@prisma/client";
import authRoutes from "./auth.js";

dotenv.config();
const app = express();
const prisma = new PrismaClient();

app.use(cors());
app.use(express.json());

// Ruta raíz
app.get("/", (req, res) => {
  res.send("✅ Servidor SistemaApp funcionando correctamente 🚀");
});

// Rutas de autenticación
app.use("/auth", authRoutes);

// Obtener todos los usuarios
app.get("/usuarios", async (req, res) => {
  const usuarios = await prisma.user.findMany();
  res.json(usuarios);
});

// Crear un usuario
app.post("/usuarios", async (req, res) => {
  const { nombre, email, password, rol } = req.body;
  try {
    const user = await prisma.user.create({
      data: { nombre, email, password, rol },
    });
    res.json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`🚀 Backend corriendo en puerto ${PORT}`));
