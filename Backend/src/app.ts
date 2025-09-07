import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
// 暂时注释掉数据库连接
// import { connectDB } from './config/database';
import experienceRoutes from './routes/experienceStatic';
import projectRoutes from './routes/projects';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// 暂时不连接MongoDB
// connectDB();

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/experience', experienceRoutes);
app.use('/api/projects', projectRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Portfolio Backend API is running' });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

export default app;
