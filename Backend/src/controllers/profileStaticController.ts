import { Request, Response } from 'express';
import { profileData } from '../data/profileData';

export const getProfileStatic = async (req: Request, res: Response) => {
  try {
    res.status(200).json({
      success: true,
      data: profileData
    });
  } catch (error) {
    console.error('Error fetching profile:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch profile data',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const updateProfileStatic = async (req: Request, res: Response) => {
  try {
    const updatedData = { ...profileData, ...req.body };
    res.status(200).json({
      success: true,
      data: updatedData,
      message: 'Profile updated successfully'
    });
  } catch (error) {
    console.error('Error updating profile:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to update profile data',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};
