import express from "express";
import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import { PrismaClient } from "@prisma/client";
import dotenv from "dotenv";

dotenv.config();
const router = express.Router();
const prisma = new PrismaClient();
const SECRET = process.env.JWT_SECRET || "clave_super_segura";

// Registro
router.post("/register", async (req, res) => {
  try {
    const { nombre, email, password, rol } = req.body;
    const existente = await prisma.user.findUnique({ where: { email } });
    if (existente) return res.status(400).json({ error: "El usuario ya existe" });

    const passwordHash = await bcrypt.hash(password, 10);
    const nuevo = await prisma.user.create({
      data: { nombre, email, passwordHash, rol },
    });

    res.json({ id: nuevo.id, nombre: nuevo.nombre, email: nuevo.email });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Login
router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) return res.status(400).json({ error: "Usuario no encontrado" });

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) return res.status(400).json({ error: "Contraseña incorrecta" });

    const token = jwt.sign(
      { id: user.id, rol: user.rol, nombre: user.nombre },
      SECRET,
      { expiresIn: "7d" }
    );

    res.json({ token, user: { id: user.id, nombre: user.nombre, rol: user.rol } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Verificar token
router.get("/verify", (req, res) => {
  const header = req.headers.authorization;
  if (!header) return res.status(401).json({ error: "Token faltante" });

  const token = header.split(" ")[1];
  try {
    const decoded = jwt.verify(token, SECRET);
    res.json({ ok: true, user: decoded });
  } catch (e) {
    res.status(401).json({ error: "Token inválido o expirado" });
  }
});

export default router;
