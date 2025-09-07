import mongoose from 'mongoose';
import dotenv from 'dotenv';
import Experience from './models/Experience';
import Project from './models/Project';

dotenv.config();

const seedData = async () => {
  try {
    // 连接数据库
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/nextmile');
    console.log('✅ Connected to MongoDB');

    // 清空现有数据
    await Experience.deleteMany({});
    await Project.deleteMany({});
    console.log('🗑️  Cleared existing data');

    // 创建工作经验数据
    const experiences = [
      {
        company: 'Apple Inc.',
        position: 'Data Science Intern',
        duration: 'Apr 2025 - Jun 2025',
        description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
        achievements: [
          'Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data from a newly launched Apple TikTok live-stream, identifying top 10 categories that informed script optimizations and resulted in a 7% reduction in return rate.',
          'Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams by leveraging A/B testing to optimize content.',
          'Informed live content strategy by applying Difference in Difference (DID) analysis to Apple\'s continuous interconnection scenarios, which resulted in a 3% boost in click-through rates and an 8.9% increase in interaction rates.'
        ],
        startDate: new Date('2025-04-01'),
        endDate: new Date('2025-06-30'),
        isCurrentJob: false,
        location: 'Cupertino, CA'
      },
      {
        company: 'Baidu Inc.',
        position: 'AI/ML Intern',
        duration: 'Dec 2024 - Mar 2025',
        description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
        achievements: [
          'Enhanced the Outline Generation module\'s performance through a multi-stage data pipeline that included model Supervised fine-tuning (LoRA), log data cleansing and annotation, resulting in an 80% win rate in GSB evaluations.',
          'Automated 40% of data annotation tasks by leveraging role-playing prompt engineering on the Deepseek-v3, also optimized 3 evaluation rules salvaging 20+% of data for valuable use.',
          'Accelerated the template update speed of Baidu Wenku\'s AI PPT Generator by leveraging LLM Fine-Tuning and post-processing strategies, achieving 90% stability and enabling the deployment of 300+ templates.',
          'Evaluated the latest LLM models(Deepseek) and applied it to text to tabular data task, achieving 95% accuracy.'
        ],
        startDate: new Date('2024-12-01'),
        endDate: new Date('2025-03-31'),
        isCurrentJob: false,
        location: 'Beijing, China'
      },
      {
        company: 'Michelin(China) Investment Co., Ltd.',
        position: 'Information Technology Intern',
        duration: 'Jun 2024 - Sep 2024',
        description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
        achievements: [
          'Automated a reseller sentiment analysis system with 75% accuracy using pre-trained Chinese Word Embedding and BiLSTM on e-commerce comments, leading to a 3.2% increase in sales.',
          'Extracted 3,000+ tire specifications from websites like Tesla and BYD by leveraging a Python Scrapy web crawler, providing crucial market data to inform product strategy for a new electric vehicle tire series.',
          'Developed a data pipeline and visualization module for SharePoint internal software by integrating and processing unstructured data sources, which drove strategic SKU selection for a new tire launch in the Asia-Pacific region.'
        ],
        startDate: new Date('2024-06-01'),
        endDate: new Date('2024-09-30'),
        isCurrentJob: false,
        location: 'Shanghai, China'
      }
    ];

    // 创建项目数据
    const projects = [
      {
        title: 'Mithril AI',
        year: 2024,
        description: 'Open science AI research lab',
        url: 'https://github.com/mithrilai',
        technologies: ['AI', 'Machine Learning', 'Research'],
        featured: true,
        githubUrl: 'https://github.com/mithrilai',
        status: 'completed'
      },
      {
        title: 'OpenDeepLearning',
        year: 2023,
        description: 'Open source AI education resources',
        url: 'https://opendeeplearning.xyz/',
        technologies: ['Education', 'AI', 'Open Source'],
        featured: true,
        liveUrl: 'https://opendeeplearning.xyz/',
        status: 'completed'
      }
    ];

    // 插入数据
    await Experience.insertMany(experiences);
    await Project.insertMany(projects);

    console.log('✅ Seed data inserted successfully');
    console.log(`📊 Created ${experiences.length} experiences and ${projects.length} projects`);

  } catch (error) {
    console.error('❌ Error seeding data:', error);
  } finally {
    await mongoose.connection.close();
    console.log('🔌 Database connection closed');
  }
};

// 运行种子数据
seedData();
