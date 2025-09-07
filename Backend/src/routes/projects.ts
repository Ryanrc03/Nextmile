import express from 'express';
import {
  getAllProjects,
  getProjectById,
  createProject,
  updateProject,
  deleteProject
} from '../controllers/projectController';

const router = express.Router();

// GET /api/projects - 获取所有项目 (支持查询参数: ?featured=true&status=completed)
router.get('/', getAllProjects);

// GET /api/projects/:id - 获取单个项目
router.get('/:id', getProjectById);

// POST /api/projects - 创建新项目
router.post('/', createProject);

// PUT /api/projects/:id - 更新项目
router.put('/:id', updateProject);

// DELETE /api/projects/:id - 删除项目
router.delete('/:id', deleteProject);

export default router;
