import Image from "next/image";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl lg:text-6xl font-bold mb-6">
              About <span className="text-[#00D9FF]">Me</span>
            </h1>
            <div className="w-24 h-1 bg-[#00D9FF] mx-auto"></div>
          </div>
          
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Left Content */}
            <div className="space-y-6">
              <p className="text-gray-300 text-lg leading-relaxed">
                I'm Creative Director and UI/UX Designer from Coimbatore, India, currently pursuing 
                a Master's degree in Computer Science at Rice University. I enjoy turning complex problems 
                into simple, beautiful and intuitive designs.
              </p>
              
              <p className="text-gray-300 text-lg leading-relaxed">
                My job is to design applications that are functional and user-friendly while maintaining 
                an attractive appearance. Moreover, I add personal touches to your product and make sure 
                that it is eye-catching and easy to use. My aim is to bring across your message and 
                identity in the most creative way.
              </p>
              
              <div className="grid grid-cols-2 gap-6 mt-8">
                <div className="bg-[#1a1a1a] p-6 rounded-xl border border-gray-800">
                  <h4 className="text-[#00D9FF] font-bold text-3xl mb-2">50+</h4>
                  <p className="text-gray-400">Projects Completed</p>
                </div>
                <div className="bg-[#1a1a1a] p-6 rounded-xl border border-gray-800">
                  <h4 className="text-[#00D9FF] font-bold text-3xl mb-2">3+</h4>
                  <p className="text-gray-400">Years Experience</p>
                </div>
              </div>
            </div>
            
            {/* Right Content - Image */}
            <div className="flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-[#00D9FF] rounded-full blur-3xl opacity-20"></div>
                <Image
                  src="/Ryan_hippocampus.png"
                  alt="Ryan Li"
                  className="relative rounded-2xl border-4 border-[#00D9FF] shadow-xl"
                  width={300}
                  height={300}
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            What I'm <span className="text-[#00D9FF]">Doing</span>
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-white mb-2">AI/ML</h3>
              <p className="text-gray-400 text-sm">Machine Learning and Artificial Intelligence development</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">💻</div>
              <h3 className="text-xl font-bold text-white mb-2">Software Development</h3>
              <p className="text-gray-400 text-sm">Full-stack development and software engineering</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-white mb-2">Data Science</h3>
              <p className="text-gray-400 text-sm">Data analysis, visualization, and insights</p>
            </div>
            
            <div className="bg-[#2a2a2a] p-6 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="text-xl font-bold text-white mb-2">Research</h3>
              <p className="text-gray-400 text-sm">Follow up cutting-edge technologies and trends</p>
            </div>
          </div>
        </div>
      </section>

      {/* Personal Info Section */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Personal <span className="text-[#00D9FF]">Information</span>
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">Name:</span>
                <span className="text-white">Ryan Rongcheng Li</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">Email:</span>
                <span className="text-white">rl182@rice.edu</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">Phone:</span>
                <span className="text-white">+1 (346) 404-7839</span>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">Location:</span>
                <span className="text-white">Houston, TX</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">University:</span>
                <span className="text-white">Rice University</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-[#00D9FF] font-semibold w-32">Status:</span>
                <span className="text-white">Open to Opportunities</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}