import type { Metadata } from "next";
import Image from "next/image";
import { experiences } from "./experience-data";

export const metadata: Metadata = {
  title: "Experiences",
  description: "Professional Experience and Projects",
};

// 公司logo映射 - 可以根据需要添加更多公司的logo
const companyLogos: { [key: string]: string } = {
  "Apple Inc.": "/company-logos/apple.png",
  "Baidu Inc.": "/company-logos/baidu.png", 
  "Michelin(China) Investment Co., Ltd.": "/company-logos/michelin.png"
};

export default function ExperiencesPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl lg:text-6xl font-bold mb-6">
              My <span className="text-[#00D9FF]">Experiences</span>
            </h1>
            <div className="w-24 h-1 bg-[#00D9FF] mx-auto mb-8"></div>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              A journey through my professional experiences in technology, 
              where I've contributed to innovative projects and developed my skills.
            </p>
          </div>
        </div>
      </section>

      {/* Experiences Section */}
      <section className="py-10 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="space-y-16">
            {experiences.map((experience, index) => (
              <div
                key={experience.id}
                className={`grid lg:grid-cols-2 gap-12 items-center ${
                  index % 2 === 1 ? 'lg:grid-flow-col-dense' : ''
                }`}
              >
                {/* Image Section */}
                <div className={`${index % 2 === 1 ? 'lg:col-start-2' : ''}`}>
                  <div className="relative bg-[#1a1a1a] rounded-2xl p-8 border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
                    {/* Company Logo Placeholder */}
                    <div className="w-32 h-32 bg-[#2a2a2a] rounded-xl mx-auto mb-6 flex items-center justify-center border-2 border-[#00D9FF]">
                      {companyLogos[experience.company] ? (
                        <Image
                          src={companyLogos[experience.company]}
                          alt={`${experience.company} logo`}
                          width={100}
                          height={100}
                          className="rounded-lg"
                        />
                      ) : (
                        <div className="text-center">
                          <div className="text-4xl text-[#00D9FF] mb-2">🏢</div>
                          <div className="text-[#00D9FF] font-bold text-sm">
                            {experience.company.split(' ')[0]}
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {/* Company Info */}
                    <div className="text-center">
                      <h3 className="text-2xl font-bold text-white mb-2">
                        {experience.company}
                      </h3>
                      <div className="bg-[#00D9FF] text-black px-4 py-1 rounded-full text-sm font-semibold inline-block mb-3">
                        {experience.duration}
                      </div>
                      <p className="text-gray-400 text-sm">
                        📍 {experience.location}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Content Section */}
                <div className={`${index % 2 === 1 ? 'lg:col-start-1' : ''}`}>
                  <div className="space-y-6">
                    <div>
                      <h2 className="text-3xl font-bold text-white mb-3">
                        {experience.position}
                      </h2>
                      <p className="text-gray-300 text-lg leading-relaxed">
                        {experience.description}
                      </p>
                    </div>

                    {/* Key Achievements */}
                    <div className="bg-[#1a1a1a] rounded-xl p-6 border border-gray-700">
                      <h4 className="text-xl font-bold text-[#00D9FF] mb-4 flex items-center">
                        <span className="mr-2">🏆</span>
                        Key Achievements
                      </h4>
                      <ul className="space-y-3">
                        {experience.achievements.map((achievement, idx) => (
                          <li key={idx} className="flex items-start space-x-3">
                            <div className="w-2 h-2 bg-[#00D9FF] rounded-full mt-2 flex-shrink-0"></div>
                            <span className="text-gray-300 leading-relaxed">{achievement}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Skills/Technologies Badge */}
                    <div className="flex flex-wrap gap-2">
                      {experience.company === "Apple Inc." && (
                        <>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Machine Learning</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">A/B Testing</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">K-Means</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">DID Analysis</span>
                        </>
                      )}
                      {experience.company === "Baidu Inc." && (
                        <>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">LLM Fine-Tuning</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">LoRA</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">DeepSeek</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Prompt Engineering</span>
                        </>
                      )}
                      {experience.company === "Michelin(China) Investment Co., Ltd." && (
                        <>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">BiLSTM</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Web Scraping</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Python Scrapy</span>
                          <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">SharePoint</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Summary Section */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12">
            Professional <span className="text-[#00D9FF]">Summary</span>
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">4+</h3>
              <p className="text-gray-400">Different Positions</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700">
              <div className="text-4xl mb-4">📅</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">12+</h3>
              <p className="text-gray-400">Months Experience</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">2+</h3>
              <p className="text-gray-400">Different Industries</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
