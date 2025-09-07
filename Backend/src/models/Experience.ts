import mongoose, { Document, Schema } from 'mongoose';

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

const ExperienceSchema: Schema = new Schema({
  company: {
    type: String,
    required: true,
    trim: true
  },
  position: {
    type: String,
    required: true,
    trim: true
  },
  duration: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  achievements: [{
    type: String,
    required: true
  }],
  startDate: {
    type: Date,
    required: true
  },
  endDate: {
    type: Date,
    required: function(this: IExperience) {
      return !this.isCurrentJob;
    }
  },
  isCurrentJob: {
    type: Boolean,
    default: false
  },
  location: {
    type: String,
    trim: true
  },
  companyLogo: {
    type: String,
    trim: true
  }
}, {
  timestamps: true
});

export default mongoose.model<IExperience>('Experience', ExperienceSchema);
