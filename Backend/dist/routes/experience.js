"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const experienceController_1 = require("../controllers/experienceController");
const router = express_1.default.Router();
// GET /api/experience - 获取所有工作经验
router.get('/', experienceController_1.getAllExperiences);
// GET /api/experience/:id - 获取单个工作经验
router.get('/:id', experienceController_1.getExperienceById);
// POST /api/experience - 创建新的工作经验
router.post('/', experienceController_1.createExperience);
// PUT /api/experience/:id - 更新工作经验
router.put('/:id', experienceController_1.updateExperience);
// DELETE /api/experience/:id - 删除工作经验
router.delete('/:id', experienceController_1.deleteExperience);
exports.default = router;
//# sourceMappingURL=experience.js.map