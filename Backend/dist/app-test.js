"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const PORT = process.env.PORT || 5000;
// Middleware
app.use((0, cors_1.default)({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true
}));
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
// Mock data for testing
const mockExperiences = [
    {
        id: '1',
        company: 'Apple Inc.',
        position: 'Data Science Intern',
        duration: 'Apr 2025 - Jun 2025',
        description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
        achievements: [
            'Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data.',
            'Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams.',
            'Informed live content strategy by applying Difference in Difference (DID) analysis.'
        ]
    },
    {
        id: '2',
        company: 'Baidu Inc.',
        position: 'AI/ML Intern',
        duration: 'Dec 2024 - Mar 2025',
        description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
        achievements: [
            'Enhanced the Outline Generation module performance through multi-stage data pipeline.',
            'Automated 40% of data annotation tasks using role-playing prompt engineering.',
            'Accelerated template update speed of Baidu Wenku AI PPT Generator.'
        ]
    }
];
const mockProjects = [
    {
        id: '1',
        title: 'Mithril AI',
        year: 2024,
        description: 'Open science AI research lab',
        url: 'https://github.com/mithrilai',
        featured: true
    },
    {
        id: '2',
        title: 'OpenDeepLearning',
        year: 2023,
        description: 'Open source AI education resources',
        url: 'https://opendeeplearning.xyz/',
        featured: true
    }
];
// Test Routes
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        message: 'Portfolio Backend API is running',
        timestamp: new Date().toISOString()
    });
});
app.get('/api/experience', (req, res) => {
    res.json({
        success: true,
        data: mockExperiences
    });
});
app.get('/api/projects', (req, res) => {
    res.json({
        success: true,
        data: mockProjects
    });
});
// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});
// 404 handler - 修复路由语法
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});
exports.default = app;
//# sourceMappingURL=app-test.js.map