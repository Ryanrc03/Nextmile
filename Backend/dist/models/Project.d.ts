import mongoose, { Document } from 'mongoose';
export interface IProject extends Document {
    title: string;
    description: string;
    year: number;
    url: string;
    technologies: string[];
    featured: boolean;
    imageUrl?: string;
    githubUrl?: string;
    liveUrl?: string;
    status: 'completed' | 'in-progress' | 'planned';
    createdAt: Date;
    updatedAt: Date;
}
declare const _default: mongoose.Model<IProject, {}, {}, {}, mongoose.Document<unknown, {}, IProject, {}, {}> & IProject & Required<{
    _id: unknown;
}> & {
    __v: number;
}, any>;
export default _default;
//# sourceMappingURL=Project.d.ts.map