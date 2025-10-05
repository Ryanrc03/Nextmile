// 静态经验数据 - 从后端 experienceData.ts 复制并调整
export interface Experience {
  id: string;
  company: string;
  position: string;
  duration: string;
  description: string;
  achievements: string[];
  location: string;
}

export const experiences: Experience[] = [
  {
    id: '1',
    company: 'Apple Inc.',
    position: 'Data Science Intern',
    duration: 'Apr 2025 - Jun 2025',
    description: 'Apple Live-streaming team.',
    achievements: [
      'Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data from a newly launched Apple TikTok live-stream, identifying top 10 categories that informed script optimizations and resulted in a 7% reduction in return rate.',
      'Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams by leveraging A/B testing to optimize content.',
      'Informed live content strategy by applying Difference in Difference (DID) analysis to Apple\'s continuous interconnection scenarios, which resulted in a 3% boost in click-through rates and an 8.9% increase in interaction rates.'
    ],
    location: 'Beijing, China'
  },
  {
    id: '2',
    company: 'Baidu Inc.',
    position: 'AI/ML Intern',
    duration: 'Dec 2024 - Mar 2025',
    description: 'Baidu Wenku AI PPT Generator team.',
    achievements: [
      'Enhanced the Outline Generation module\'s performance through a multi-stage data pipeline that included model Supervised fine-tuning (LoRA), log data cleansing and annotation, resulting in an 80% win rate in GSB evaluations.',
      'Automated 40% of data annotation tasks by leveraging role-playing prompt engineering on the Deepseek-v3, also optimized 3 evaluation rules salvaging 20+% of data for valuable use.',
      'Accelerated the template update speed of Baidu Wenku\'s AI PPT Generator by leveraging LLM Fine-Tuning and post-processing strategies, achieving 90% stability and enabling the deployment of 300+ templates.',
      'Evaluated the latest LLM models(Deepseek) and applied it to text to tabular data task, achieving 95% accuracy.'
    ],
    location: 'Beijing, China'
  },
  {
    id: '3',
    company: 'Michelin(China) Investment Co., Ltd.',
    position: 'Information Technology Intern',
    duration: 'Jun 2024 - Sep 2024',
    description: 'Production Marketing China Team.',
    achievements: [
      'Automated a reseller sentiment analysis system with 75% accuracy using pre-trained Chinese Word Embedding and BiLSTM on e-commerce comments, leading to a 3.2% increase in sales.',
      'Extracted 3,000+ tire specifications from websites like Tesla and BYD by leveraging a Python Scrapy web crawler, providing crucial market data to inform product strategy for a new electric vehicle tire series.',
      'Developed a data pipeline and visualization module for SharePoint internal software by integrating and processing unstructured data sources, which drove strategic SKU selection for a new tire launch in the Asia-Pacific region.'
    ],
    location: 'Shanghai, China'
  }
];
