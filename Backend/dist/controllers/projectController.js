"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteProject = exports.updateProject = exports.createProject = exports.getProjectById = exports.getAllProjects = void 0;
const Project_1 = __importDefault(require("../models/Project"));
const getAllProjects = async (req, res) => {
    try {
        const { featured, status } = req.query;
        let filter = {};
        if (featured === 'true') {
            filter.featured = true;
        }
        if (status) {
            filter.status = status;
        }
        const projects = await Project_1.default.find(filter).sort({ year: -1, createdAt: -1 });
        res.json({
            success: true,
            data: projects
        });
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch projects'
        });
    }
};
exports.getAllProjects = getAllProjects;
const getProjectById = async (req, res) => {
    try {
        const project = await Project_1.default.findById(req.params.id);
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
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch project'
        });
    }
};
exports.getProjectById = getProjectById;
const createProject = async (req, res) => {
    try {
        const project = new Project_1.default(req.body);
        await project.save();
        res.status(201).json({
            success: true,
            data: project
        });
    }
    catch (error) {
        res.status(400).json({
            success: false,
            error: 'Failed to create project'
        });
    }
};
exports.createProject = createProject;
const updateProject = async (req, res) => {
    try {
        const project = await Project_1.default.findByIdAndUpdate(req.params.id, req.body, { new: true, runValidators: true });
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
    }
    catch (error) {
        res.status(400).json({
            success: false,
            error: 'Failed to update project'
        });
    }
};
exports.updateProject = updateProject;
const deleteProject = async (req, res) => {
    try {
        const project = await Project_1.default.findByIdAndDelete(req.params.id);
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
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to delete project'
        });
    }
};
exports.deleteProject = deleteProject;
//# sourceMappingURL=projectController.js.map