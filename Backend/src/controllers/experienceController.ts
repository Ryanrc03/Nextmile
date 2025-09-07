import { Request, Response } from 'express';
import Experience from '../models/Experience';

export const getAllExperiences = async (req: Request, res: Response): Promise<void> => {
  try {
    const experiences = await Experience.find().sort({ startDate: -1 });
    res.json({
      success: true,
      data: experiences
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch experiences'
    });
  }
};

export const getExperienceById = async (req: Request, res: Response): Promise<void> => {
  try {
    const experience = await Experience.findById(req.params.id);
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

export const createExperience = async (req: Request, res: Response): Promise<void> => {
  try {
    const experience = new Experience(req.body);
    await experience.save();
    res.status(201).json({
      success: true,
      data: experience
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: 'Failed to create experience'
    });
  }
};

export const updateExperience = async (req: Request, res: Response): Promise<void> => {
  try {
    const experience = await Experience.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
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
    res.status(400).json({
      success: false,
      error: 'Failed to update experience'
    });
  }
};

export const deleteExperience = async (req: Request, res: Response): Promise<void> => {
  try {
    const experience = await Experience.findByIdAndDelete(req.params.id);
    if (!experience) {
      res.status(404).json({
        success: false,
        error: 'Experience not found'
      });
      return;
    }
    res.json({
      success: true,
      message: 'Experience deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete experience'
    });
  }
};
