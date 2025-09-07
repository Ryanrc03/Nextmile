'use client';

import { useState, useEffect } from 'react';

// 定义Experience类型
interface Experience {
  id: string;
  company: string;
  position: string;
  duration: string;
  description: string;
  achievements: string[];
  location?: string;
}

// Experience组件 - 保持原来的完整设计框架
function ExperienceCard({ experience }: { experience: Experience }) {
  return (
    <div className="mb-8 space-y-6 max-w-4xl mx-auto">
      <div className="flex flex-col md:flex-row items-center gap-6 p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-h-72 mx-auto w-full">
        <div className="md:w-full">
          <div className="pl-4 bg-gray-50 dark:bg-neutral-900 rounded-xl shadow-sm border-l-4 border-black/10 dark:border-white/10 p-4">
            <h3 className="text-lg font-semibold mb-1 text-gray-900 dark:text-gray-100">
              {experience.company}
            </h3>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-2">
              {experience.duration}
            </p>
            <p className="mb-3 text-sm text-neutral-800 dark:text-neutral-200">
              {experience.position} — {experience.description}
            </p>
            <ul className="list-disc list-inside text-sm space-y-1 pl-2 text-neutral-700 dark:text-neutral-300">
              {experience.achievements.map((achievement, index) => (
                <li key={index}>{achievement}</li>
              ))}
            </ul>
            {experience.location && (
              <p className="mt-2 text-xs text-neutral-500 dark:text-neutral-400">
                📍 {experience.location}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ExperienceClient() {
  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchExperiences() {
      try {
        setLoading(true);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
        
        const res = await fetch(`${apiUrl}/api/experience`);
        
        if (!res.ok) {
          throw new Error(`Failed to fetch experiences: ${res.status} ${res.statusText}`);
        }
        
        const data = await res.json();
        setExperiences(data.data || []);
      } catch (error) {
        console.error('Error fetching experiences:', error);
        // 如果API失败，使用静态数据作为备用
        const fallbackData = [
          {
            id: '1',
            company: 'Apple Inc.',
            position: 'Data Science Intern',
            duration: 'Apr 2025 - Jun 2025',
            description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
            achievements: [
              'Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data from a newly launched Apple TikTok live-stream, identifying top 10 categories that informed script optimizations and resulted in a 7% reduction in return rate.',
              'Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams by leveraging A/B testing to optimize content.',
              'Informed live content strategy by applying Difference in Difference (DID) analysis to Apple\'s continuous interconnection scenarios, which resulted in a 3% boost in click-through rates and an 8.9% increase in interaction rates.'
            ],
            location: 'Cupertino, CA'
          },
          {
            id: '2',
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
            location: 'Beijing, China'
          },
          {
            id: '3',
            company: 'Michelin(China) Investment Co., Ltd.',
            position: 'Information Technology Intern',
            duration: 'Jun 2024 - Sep 2024',
            description: 'Contributed to cutting-edge projects in machine learning and data analysis.',
            achievements: [
              'Automated a reseller sentiment analysis system with 75% accuracy using pre-trained Chinese Word Embedding and BiLSTM on e-commerce comments, leading to a 3.2% increase in sales.',
              'Extracted 3,000+ tire specifications from websites like Tesla and BYD by leveraging a Python Scrapy web crawler, providing crucial market data to inform product strategy for a new electric vehicle tire series.',
              'Developed a data pipeline and visualization module for SharePoint internal software by integrating and processing unstructured data sources, which drove strategic SKU selection for a new tire launch in the Asia-Pacific region.'
            ],
            location: 'Shanghai, China'
          }
        ];
        setExperiences(fallbackData);
        setError(null); // 不显示错误，因为我们有备用数据
      } finally {
        setLoading(false);
      }
    }

    fetchExperiences();
  }, []);

  if (loading) {
    return (
      <div className="prose prose-neutral dark:prose-invert">
        <div className="text-center py-8">
          <p className="text-neutral-600 dark:text-neutral-400">Loading experiences...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="prose prose-neutral dark:prose-invert">
      {experiences.map((experience) => (
        <ExperienceCard key={experience.id} experience={experience} />
      ))}
    </div>
  );
}
