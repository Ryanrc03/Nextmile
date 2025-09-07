"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const dotenv_1 = __importDefault(require("dotenv"));
// 暂时注释掉数据库连接
// import { connectDB } from './config/database';
const experienceStatic_1 = __importDefault(require("./routes/experienceStatic"));
const projects_1 = __importDefault(require("./routes/projects"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const PORT = process.env.PORT || 5000;
// 暂时不连接MongoDB
// connectDB();
// Middleware
app.use((0, cors_1.default)({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true
}));
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
// Routes
app.use('/api/experience', experienceStatic_1.default);
app.use('/api/projects', projects_1.default);
// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'Portfolio Backend API is running' });
});
// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});
// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});
exports.default = app;
//# sourceMappingURL=app.js.map