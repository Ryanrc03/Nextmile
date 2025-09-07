"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const projectController_1 = require("../controllers/projectController");
const router = express_1.default.Router();
// GET /api/projects - 获取所有项目 (支持查询参数: ?featured=true&status=completed)
router.get('/', projectController_1.getAllProjects);
// GET /api/projects/:id - 获取单个项目
router.get('/:id', projectController_1.getProjectById);
// POST /api/projects - 创建新项目
router.post('/', projectController_1.createProject);
// PUT /api/projects/:id - 更新项目
router.put('/:id', projectController_1.updateProject);
// DELETE /api/projects/:id - 删除项目
router.delete('/:id', projectController_1.deleteProject);
exports.default = router;
//# sourceMappingURL=projects.js.map