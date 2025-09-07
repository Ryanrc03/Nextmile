import express from 'express';
import {
  getAllExperiences,
  getExperienceById,
  createExperience,
  updateExperience,
  deleteExperience
} from '../controllers/experienceController';

const router = express.Router();

// GET /api/experience - 获取所有工作经验
router.get('/', getAllExperiences);

// GET /api/experience/:id - 获取单个工作经验
router.get('/:id', getExperienceById);

// POST /api/experience - 创建新的工作经验
router.post('/', createExperience);

// PUT /api/experience/:id - 更新工作经验
router.put('/:id', updateExperience);

// DELETE /api/experience/:id - 删除工作经验
router.delete('/:id', deleteExperience);

export default router;
