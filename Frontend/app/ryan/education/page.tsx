export default function EducationPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="flex items-center justify-center space-x-4 mb-6">
              <div className="w-12 h-12 bg-[#00D9FF] rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z"/>
                </svg>
              </div>
              <h1 className="text-5xl lg:text-6xl font-bold">Education</h1>
            </div>
            <div className="w-24 h-1 bg-[#00D9FF] mx-auto"></div>
          </div>
        </div>
      </section>

      {/* Education Timeline */}
      <section className="py-10 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto">
          
          {/* Rice University */}
          <div className="bg-[#1a1a1a] rounded-xl p-8 mb-8 border border-gray-800 hover:border-[#00D9FF] transition-all duration-300">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between">
              <div className="flex-1">
                <h2 className="text-3xl font-bold text-white mb-3">
                  RICE UNIVERSITY
                </h2>
                <div className="flex items-center space-x-4 mb-4">
                  <span className="bg-[#00D9FF] text-black px-4 py-1 rounded-full text-sm font-semibold">
                    Aug 2025- Dec 2026
                  </span>
                </div>
                <p className="text-xl text-gray-300 mb-2 font-semibold">
                  Master of Computer Science
                </p>
                <p className="text-gray-400 mb-4">
                  Specializing in Machine Learning, Artificial Intelligence, and Software Engineering. 
                  Currently maintaining a strong academic record while engaging in cutting-edge research 
                  in AI/ML applications.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Machine Learning</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Deep Learning</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Software Engineering</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Data Science</span>
                </div>
              </div>
            </div>
          </div>

          {/* Hong Kong Baptist University */}
          <div className="bg-[#1a1a1a] rounded-xl p-8 mb-8 border border-gray-800 hover:border-[#00D9FF] transition-all duration-300">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between">
              <div className="flex-1">
                <h2 className="text-3xl font-bold text-white mb-3">
                  HONG KONG BAPTIST UNIVERSITY
                </h2>
                <div className="flex items-center space-x-4 mb-4">
                  <span className="bg-gray-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Sep 2021- Jun 2025
                  </span>
                </div>
                <p className="text-xl text-gray-300 mb-2 font-semibold">
                  Bachelor of Computer Science
                </p>
                <p className="text-gray-400 mb-4">
                  Comprehensive foundation in computer science fundamentals including algorithms, 
                  data structures, software development, and system design. Graduated with First class honor.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Algorithms</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Data Structures</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Software Development</span>
                  <span className="bg-[#2a2a2a] text-[#00D9FF] px-3 py-1 rounded-full text-sm">Database Systems</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Certifications & Courses */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Certifications & <span className="text-[#00D9FF]">Courses</span>
          </h2>
          
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-[#00D9FF]"></div>
            
            <div className="space-y-12">
              {/* Course 1 */}
              <div className="flex items-start space-x-8">
                <div className="w-4 h-4 bg-[#00D9FF] rounded-full mt-2 relative z-10"></div>
                <div className="flex-1 bg-[#2a2a2a] rounded-xl p-6 border border-gray-700">
                  <h3 className="text-2xl font-bold text-white mb-2">
                    Mastering Figma: Beginner to Expert UI/UX Design
                  </h3>
                  <p className="text-gray-400 text-sm mb-3">
                    GUVI • Verify certificate at: www.guvi.in/certificate?id=e1c51o35987111f78q
                  </p>
                  <p className="text-gray-300">
                    Comprehensive UI/UX design course covering design principles, prototyping, 
                    user research, and modern design tools.
                  </p>
                </div>
              </div>

              {/* Course 2 */}
              <div className="flex items-start space-x-8">
                <div className="w-4 h-4 bg-[#00D9FF] rounded-full mt-2 relative z-10"></div>
                <div className="flex-1 bg-[#2a2a2a] rounded-xl p-6 border border-gray-700">
                  <h3 className="text-2xl font-bold text-white mb-2">
                    FIGMA DESIGN COURSE
                  </h3>
                  <p className="text-gray-400 text-sm mb-3">
                    UDEMY • ude.my/UC-6a62b02-9266-4033-9843-3d88071tc341
                  </p>
                  <p className="text-gray-300">
                    Advanced Figma techniques for professional UI/UX design, including 
                    component systems, auto-layout, and collaborative design workflows.
                  </p>
                </div>
              </div>

              {/* Course 3 */}
              <div className="flex items-start space-x-8">
                <div className="w-4 h-4 bg-[#00D9FF] rounded-full mt-2 relative z-10"></div>
                <div className="flex-1 bg-[#2a2a2a] rounded-xl p-6 border border-gray-700">
                  <h3 className="text-2xl font-bold text-white mb-2">
                    INTRODUCTION TO GRAPHIC DESIGN WITH PHOTOSHOP
                  </h3>
                  <p className="text-gray-400 text-sm mb-3">
                    GREAT LEARNING Academy
                  </p>
                  <p className="text-gray-300">
                    Fundamental graphic design principles and practical Photoshop skills 
                    for creating visual content and digital artwork.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills & Technologies */}
      {/* <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Technical <span className="text-[#00D9FF]">Skills</span>
          </h2> */}
          
          {/* <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Programming Languages */}
            {/* <div className="bg-[#1a1a1a] p-6 rounded-xl border border-gray-800">
              <h3 className="text-xl font-bold text-[#00D9FF] mb-4">Programming Languages</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white">Python</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[98%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">JavaScript/TypeScript</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[80%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">C/C++</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[70%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">Latex</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[90%]"></div>
                  </div>
                </div>
              </div>
            </div> */} 

            {/* Frameworks & Tools */}
            {/* <div className="bg-[#1a1a1a] p-6 rounded-xl border border-gray-800">
              <h3 className="text-xl font-bold text-[#00D9FF] mb-4">Frameworks & Tools</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white">PyTorch</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[95%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">React/Next.js</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[70%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white"></span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[80%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">Docker</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[50%]"></div>
                  </div>
                </div>
              </div>
            </div> */}

            {/* Design Tools */}
            {/* <div className="bg-[#1a1a1a] p-6 rounded-xl border border-gray-800">
              <h3 className="text-xl font-bold text-[#00D9FF] mb-4">Design Tools</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white">Figma</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[95%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">Photoshop</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[85%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">Illustrator</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[80%]"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white">Canva</span>
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full w-[90%]"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section> */}

      {/* Academic Achievements */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Academic <span className="text-[#00D9FF]">Achievements</span>
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center">
              <div className="text-4xl mb-4">🎓</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">90%+</h3>
              <p className="text-gray-400">Current GPA</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">30+</h3>
              <p className="text-gray-400">Courses Completed</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center">
              <div className="text-4xl mb-4">🏆</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">5+</h3>
              <p className="text-gray-400">Certifications</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center">
              <div className="text-4xl mb-4">🔬</div>
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-2">3+</h3>
              <p className="text-gray-400">Research Projects</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}