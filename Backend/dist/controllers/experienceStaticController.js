"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getExperienceByCompanyStatic = exports.getExperienceByIdStatic = exports.getAllExperiencesStatic = void 0;
const experienceData_1 = require("../data/experienceData");
// 使用静态数据的控制器（不依赖MongoDB）
const getAllExperiencesStatic = async (req, res) => {
    try {
        // 按开始日期排序（最新的在前）
        const sortedExperiences = experienceData_1.experienceData.sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime());
        res.json({
            success: true,
            data: sortedExperiences,
            count: sortedExperiences.length
        });
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch experiences'
        });
    }
};
exports.getAllExperiencesStatic = getAllExperiencesStatic;
const getExperienceByIdStatic = async (req, res) => {
    try {
        const { id } = req.params;
        const experience = experienceData_1.experienceData.find(exp => exp.id === id);
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
exports.getExperienceByIdStatic = getExperienceByIdStatic;
const getExperienceByCompanyStatic = async (req, res) => {
    try {
        const { company } = req.params;
        const experiences = experienceData_1.experienceData.filter(exp => exp.company.toLowerCase().includes(company.toLowerCase()));
        res.json({
            success: true,
            data: experiences,
            count: experiences.length
        });
    }
    catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to fetch experiences by company'
        });
    }
};
exports.getExperienceByCompanyStatic = getExperienceByCompanyStatic;
//# sourceMappingURL=experienceStaticController.js.map