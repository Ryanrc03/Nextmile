export interface Project {
  type: string;
  company: string;
  position: string;
  description: string;
  technologies: string;
  year?: number;
}

export const projects: Project[] = [
  {
    type: "intern",
    company: "Baidu Inc.",
    position: "AI/ML Engineer",
    description: "Enhanced the Outline Generation module's performance through a multi-stage data pipeline that included model Supervised fine-tuning (LoRA), log data cleansing and annotation, resulting in an 80% win rate in GSB evaluations.",
    technologies: "LoRA, Data Pipeline, Model Fine-tuning",
    year: 2024
  },
  {
    type: "intern",
    company: "Baidu Inc.",
    position: "AI/ML Engineer",
    description: "Automated 40% of data annotation tasks by leveraging role-playing prompt engineering on the Deepseek-v3, also optimized 3 evaluation rules salvaging 20+% of data for valuable use.",
    technologies: "Deepseek-v3, Prompt Engineering",
    year: 2024
  },
  {
    type: "intern",
    company: "Baidu Inc.",
    position: "AI/ML Engineer",
    description: "Accelerated the template update speed of Baidu Wenku's AI PPT Generator by leveraging LLM Fine-Tuning and post processing strategies, achieving 90% stability and enabling the deployment of 300+ templates.",
    technologies: "LLM Fine-Tuning, Post Processing",
    year: 2024
  },
  {
    type: "intern",
    company: "Baidu Inc.",
    position: "AI/ML Engineer",
    description: "Evaluated the latest LLM models(Deepseek) and applied it to text to tabular data task, achieving 95% accuracy.",
    technologies: "Deepseek, LLM Evaluation",
    year: 2024
  },
  {
    type: "intern",
    company: "Apple Inc.",
    position: "Data Scientist",
    description: "Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data from a newly launched Apple TikTok live-stream, identifying top 10 categories that informed script optimizations and resulted in a 7% reduction in return rate.",
    technologies: "Word Embedding, MiniBatch K-Means, Real-time Data Analysis",
    year: 2024
  },
  {
    type: "intern",
    company: "Apple Inc.",
    position: "Data Scientist",
    description: "Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams by leveraging A/B testing to optimize content.",
    technologies: "A/B Testing, Content Optimization",
    year: 2024
  },
  {
    type: "intern",
    company: "Apple Inc.",
    position: "Data Scientist",
    description: "Informed live content strategy by applying Difference in Difference(DID) analysis to Apple's continuous interconnection scenarios, which resulted in a 3% boost in click-through rates and an 8.9% increase in interaction rates.",
    technologies: "Difference in Difference Analysis, Statistical Analysis",
    year: 2024
  },
  {
    type: "intern",
    company: "Michelin(China) Investment Co. Ltd.",
    position: "Information Technology Intern",
    description: "Automated a reseller sentiment analysis system with 75% accuracy using pre-trained Chinese Word Embedding and BiLSTM on e-commerce comments, leading to a 3.2% increase in sales.",
    technologies: "Chinese Word Embedding, BiLSTM, Sentiment Analysis",
    year: 2023
  },
  {
    type: "intern",
    company: "Michelin(China) Investment Co. Ltd.",
    position: "Information Technology Intern",
    description: "Extracted 3000+ tire specifications from websites like Tesla and BYD by leveraging a Python Scrapy web crawler, providing crucial market data to inform product strategy for a new electric vehicle tire series.",
    technologies: "Python, Scrapy, Web Crawling",
    year: 2023
  },
  {
    type: "intern",
    company: "Michelin(China) Investment Co. Ltd.",
    position: "Information Technology Intern",
    description: "Developed a data pipeline and visualization module for SharePoint internal software by integrating and processing unstructured data sources, which drove strategic SKU selection for a new tire launch in the Asia-Pacific region.",
    technologies: "Data Pipeline, SharePoint, Data Visualization",
    year: 2023
  },
  {
    type: "Project",
    company: "Machine Learning Course",
    position: "A Deep Reinforcement Learning Based Stock Automated Trading System",
    description: "Developed a Deep Deterministic Policy Gradient-based automated trading agent, leveraging advanced data preprocessing to improve annual returns by 10% in backtesting scenarios.",
    technologies: "Deep Reinforcement Learning, DDPG, Data Preprocessing",
    year: 2023
  },
  {
    type: "Project",
    company: "Undergraduate Research",
    position: "Facial Emotion Recognition System",
    description: "Developed a CNN-based facial emotion classifier with 80% accuracy on the FER-2013 dataset. Integrated the classifier into an interactive PyQt5 system to analyze emotional data and visualize insights. Award: Excellent Award.",
    technologies: "CNN, PyQt5, FER-2013 Dataset, Data Visualization, Emotion Analysis",
    year: 2022
  }
];
