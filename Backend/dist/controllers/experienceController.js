"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteExperience = exports.updateExperience = exports.createExperience = exports.getExperienceById = exports.getAllExperiences = void 0;
const Experience_1 = __importDefault(require("../models/Experience"));
const getAllExperiences = async (req, res) => {
    try {
        const experiences = await Experience_1.default.find().sort({ startDate: -1 });
        res.json({
            success: true,
            data: experiences
        });
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch experiences'
        });
    }
};
exports.getAllExperiences = getAllExperiences;
const getExperienceById = async (req, res) => {
    try {
        const experience = await Experience_1.default.findById(req.params.id);
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
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch experience'
        });
    }
};
exports.getExperienceById = getExperienceById;
const createExperience = async (req, res) => {
    try {
        const experience = new Experience_1.default(req.body);
        await experience.save();
        res.status(201).json({
            success: true,
            data: experience
        });
    }
    catch (error) {
        res.status(400).json({
            success: false,
            error: 'Failed to create experience'
        });
    }
};
exports.createExperience = createExperience;
const updateExperience = async (req, res) => {
    try {
        const experience = await Experience_1.default.findByIdAndUpdate(req.params.id, req.body, { new: true, runValidators: true });
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
    }
    catch (error) {
        res.status(400).json({
            success: false,
            error: 'Failed to update experience'
        });
    }
};
exports.updateExperience = updateExperience;
const deleteExperience = async (req, res) => {
    try {
        const experience = await Experience_1.default.findByIdAndDelete(req.params.id);
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
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to delete experience'
        });
    }
};
exports.deleteExperience = deleteExperience;
//# sourceMappingURL=experienceController.js.map