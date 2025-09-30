export default function SkillsPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl lg:text-6xl font-bold mb-6">
              MY <span className="text-[#00D9FF]">SKILLS</span>:
            </h1>
            <div className="w-24 h-1 bg-[#00D9FF] mx-auto"></div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="py-10 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto">
          
          {/* Skills Card */}
          <div className="bg-[#1a1a1a] rounded-xl p-12 border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
            <div className="space-y-8">
              
              {/* Application designing */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white text-lg font-medium">AI/ML Development & Optimization</span>
                  <span className="text-[#00D9FF] font-bold">90%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div className="bg-gradient-to-r from-[#A0D911] to-[#52C41A] h-3 rounded-full transition-all duration-1000 ease-out" style={{width: '90%'}}></div>
                </div>
              </div>

              {/* Figma software */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white text-lg font-medium">Software Development</span>
                  <span className="text-[#00D9FF] font-bold">85%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div className="bg-gradient-to-r from-[#A0D911] to-[#52C41A] h-3 rounded-full transition-all duration-1000 ease-out" style={{width: '85%'}}></div>
                </div>
              </div>

              {/* Website design */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white text-lg font-medium">Data Analysis</span>
                  <span className="text-[#00D9FF] font-bold">80%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div className="bg-gradient-to-r from-[#A0D911] to-[#52C41A] h-3 rounded-full transition-all duration-1000 ease-out" style={{width: '80%'}}></div>
                </div>
              </div>

              {/* UX writing */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white text-lg font-medium">Research</span>
                  <span className="text-[#00D9FF] font-bold">80%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div className="bg-gradient-to-r from-[#A0D911] to-[#52C41A] h-3 rounded-full transition-all duration-1000 ease-out" style={{width: '80%'}}></div>
                </div>
              </div>

            </div>
          </div>
          
        </div>
      </section>

      {/* Technical Skills Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Technical <span className="text-[#00D9FF]">Skills</span>
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            
            {/* Programming Languages */}
            <div className="bg-[#1a1a1a] p-8 rounded-xl border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-6">AI/ML</h3>
              <div className="space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Pytorch</span>
                    <span className="text-[#00D9FF] font-bold">95%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '95%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Numpy</span>
                    <span className="text-[#00D9FF] font-bold">88%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '88%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Linux</span>
                    <span className="text-[#00D9FF] font-bold">82%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '82%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">CUDA</span>
                    <span className="text-[#00D9FF] font-bold">78%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '78%'}}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Frameworks & Libraries */}
            <div className="bg-[#1a1a1a] p-8 rounded-xl border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-6">Software Development</h3>
              <div className="space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">React/Next.js</span>
                    <span className="text-[#00D9FF] font-bold">90%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '90%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Database</span>
                    <span className="text-[#00D9FF] font-bold">85%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '85%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">AI Copilot</span>
                    <span className="text-[#00D9FF] font-bold">99%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '99%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Docker & Cloud Computing</span>
                    <span className="text-[#00D9FF] font-bold">60%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '60%'}}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Tools & Technologies */}
            <div className="bg-[#1a1a1a] p-8 rounded-xl border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
              <h3 className="text-2xl font-bold text-[#00D9FF] mb-6">Data Analysis</h3>
              <div className="space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Visualization</span>
                    <span className="text-[#00D9FF] font-bold">95%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '95%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Causal Inference</span>
                    <span className="text-[#00D9FF] font-bold">60%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '60%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">AB Testing</span>
                    <span className="text-[#00D9FF] font-bold">75%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '75%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium">Statistics</span>
                    <span className="text-[#00D9FF] font-bold">85%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-[#00D9FF] h-2 rounded-full transition-all duration-1000 ease-out" style={{width: '85%'}}></div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Soft Skills Section */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Soft <span className="text-[#00D9FF]">Skills</span>
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-white mb-2">Problem Solving</h3>
              <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                <div className="bg-[#00D9FF] h-2 rounded-full" style={{width: '95%'}}></div>
              </div>
              <p className="text-[#00D9FF] font-bold">95%</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">👥</div>
              <h3 className="text-xl font-bold text-white mb-2">Team Work</h3>
              <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                <div className="bg-[#00D9FF] h-2 rounded-full" style={{width: '90%'}}></div>
              </div>
              <p className="text-[#00D9FF] font-bold">90%</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-xl font-bold text-white mb-2">Communication</h3>
              <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                <div className="bg-[#00D9FF] h-2 rounded-full" style={{width: '88%'}}></div>
              </div>
              <p className="text-[#00D9FF] font-bold">88%</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-xl font-bold text-white mb-2">Leadership</h3>
              <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                <div className="bg-[#00D9FF] h-2 rounded-full" style={{width: '85%'}}></div>
              </div>
              <p className="text-[#00D9FF] font-bold">85%</p>
            </div>
          </div>
        </div>
      </section>

      {/* Languages Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            <span className="text-[#00D9FF]">Languages</span>
          </h2>
          
          <div className="bg-[#1a1a1a] rounded-xl p-8 border border-gray-700 hover:border-[#00D9FF] transition-all duration-300">
            <div className="grid md:grid-cols-2 gap-8">
              
              <div className="space-y-6">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">English</span>
                    <span className="text-[#00D9FF] font-bold">Fluent</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div className="bg-[#00D9FF] h-3 rounded-full" style={{width: '95%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Chinese (Mandarin)</span>
                    <span className="text-[#00D9FF] font-bold">Native</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div className="bg-[#00D9FF] h-3 rounded-full" style={{width: '100%'}}></div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-6">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Cantonese</span>
                    <span className="text-[#00D9FF] font-bold">Learning</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div className="bg-[#00D9FF] h-3 rounded-full" style={{width: '40%'}}></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Teochew</span>
                    <span className="text-[#00D9FF] font-bold">Learning</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div className="bg-[#00D9FF] h-3 rounded-full" style={{width: '30%'}}></div>
                  </div>
                </div>
              </div>
              
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}