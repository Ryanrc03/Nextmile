import mongoose, { Document } from 'mongoose';
export interface IExperience extends Document {
    company: string;
    position: string;
    duration: string;
    description: string;
    achievements: string[];
    startDate: Date;
    endDate?: Date;
    isCurrentJob: boolean;
    location?: string;
    companyLogo?: string;
    createdAt: Date;
    updatedAt: Date;
}
declare const _default: mongoose.Model<IExperience, {}, {}, {}, mongoose.Document<unknown, {}, IExperience, {}, {}> & IExperience & Required<{
    _id: unknown;
}> & {
    __v: number;
}, any>;
export default _default;
//# sourceMappingURL=Experience.d.ts.map