"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const app_test_1 = __importDefault(require("./app-test"));
const PORT = process.env.PORT || 5000;
app_test_1.default.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
    console.log(`💼 Experience API: http://localhost:${PORT}/api/experience`);
    console.log(`🎯 Projects API: http://localhost:${PORT}/api/projects`);
});
//# sourceMappingURL=server-test.js.map