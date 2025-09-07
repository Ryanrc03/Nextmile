import { Request, Response } from 'express';
import Project from '../models/Project';

export const getAllProjects = async (req: Request, res: Response): Promise<void> => {
  try {
    const { featured, status } = req.query;
    let filter: any = {};
    
    if (featured === 'true') {
      filter.featured = true;
    }
    
    if (status) {
      filter.status = status;
    }
    
    const projects = await Project.find(filter).sort({ year: -1, createdAt: -1 });
    res.json({
      success: true,
      data: projects
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch projects'
    });
  }
};

export const getProjectById = async (req: Request, res: Response): Promise<void> => {
  try {
    const project = await Project.findById(req.params.id);
    if (!project) {
      res.status(404).json({
        success: false,
        error: 'Project not found'
      });
      return;
    }
    res.json({
      success: true,
      data: project
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch project'
    });
  }
};

export const createProject = async (req: Request, res: Response): Promise<void> => {
  try {
    const project = new Project(req.body);
    await project.save();
    res.status(201).json({
      success: true,
      data: project
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: 'Failed to create project'
    });
  }
};

export const updateProject = async (req: Request, res: Response): Promise<void> => {
  try {
    const project = await Project.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
    if (!project) {
      res.status(404).json({
        success: false,
        error: 'Project not found'
      });
      return;
    }
    res.json({
      success: true,
      data: project
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: 'Failed to update project'
    });
  }
};

export const deleteProject = async (req: Request, res: Response): Promise<void> => {
  try {
    const project = await Project.findByIdAndDelete(req.params.id);
    if (!project) {
      res.status(404).json({
        success: false,
        error: 'Project not found'
      });
      return;
    }
    res.json({
      success: true,
      message: 'Project deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete project'
    });
  }
};
