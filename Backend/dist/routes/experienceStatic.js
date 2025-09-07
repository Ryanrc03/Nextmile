"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const experienceStaticController_1 = require("../controllers/experienceStaticController");
const router = express_1.default.Router();
// GET /api/experience - 获取所有工作经验（使用静态数据）
router.get('/', experienceStaticController_1.getAllExperiencesStatic);
// GET /api/experience/:id - 获取单个工作经验
router.get('/:id', experienceStaticController_1.getExperienceByIdStatic);
// GET /api/experience/company/:company - 按公司名称查找经验
router.get('/company/:company', experienceStaticController_1.getExperienceByCompanyStatic);
exports.default = router;
//# sourceMappingURL=experienceStatic.js.map