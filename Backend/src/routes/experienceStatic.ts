import express from 'express';
import {
  getAllExperiencesStatic,
  getExperienceByIdStatic,
  getExperienceByCompanyStatic
} from '../controllers/experienceStaticController';

const router = express.Router();

// GET /api/experience - 获取所有工作经验（使用静态数据）
router.get('/', getAllExperiencesStatic);

// GET /api/experience/:id - 获取单个工作经验
router.get('/:id', getExperienceByIdStatic);

// GET /api/experience/company/:company - 按公司名称查找经验
router.get('/company/:company', getExperienceByCompanyStatic);

export default router;
