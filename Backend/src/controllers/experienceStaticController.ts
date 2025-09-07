import { Request, Response } from 'express';
import { experienceData } from '../data/experienceData';

// 使用静态数据的控制器（不依赖MongoDB）
export const getAllExperiencesStatic = async (req: Request, res: Response): Promise<void> => {
  try {
    // 按开始日期排序（最新的在前）
    const sortedExperiences = experienceData.sort((a, b) => 
      new Date(b.startDate).getTime() - new Date(a.startDate).getTime()
    );
    
    res.json({
      success: true,
      data: sortedExperiences,
      count: sortedExperiences.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch experiences'
    });
  }
};

export const getExperienceByIdStatic = async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;
    const experience = experienceData.find(exp => exp.id === id);
    
    if (!experience) {
      res.status(404).json({
        success: false,
        error: 'Experience not found'
      });
      return;
    }
    
    res.json({
      success: true,
      data: experience
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch experience'
    });
  }
};

export const getExperienceByCompanyStatic = async (req: Request, res: Response): Promise<void> => {
  try {
    const { company } = req.params;
    const experiences = experienceData.filter(exp => 
      exp.company.toLowerCase().includes(company.toLowerCase())
    );
    
    res.json({
      success: true,
      data: experiences,
      count: experiences.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch experiences by company'
    });
  }
};
