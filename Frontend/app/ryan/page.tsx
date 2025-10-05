import Image from "next/image";

export default function RyanPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-20 left-20 w-0 h-0 border-l-[50px] border-l-transparent border-b-[80px] border-b-white border-r-[50px] border-r-transparent rotate-180"></div>
      <div className="absolute bottom-20 left-1/3 w-0 h-0 border-l-[30px] border-l-transparent border-b-[60px] border-b-white border-r-[30px] border-r-transparent"></div>
      <div className="absolute bottom-32 right-20 w-0 h-0 border-l-[40px] border-l-transparent border-b-[70px] border-b-white border-r-[40px] border-r-transparent rotate-45"></div>
      
      {/* Main content */}
      <div className="max-w-7xl mx-auto px-8 lg:px-16 pt-32 pb-20">
        <div className="grid lg:grid-cols-2 gap-16 items-center min-h-[80vh]">
          
          {/* Left Content */}
          <div className="space-y-8">
            <h2 className="text-6xl lg:text-7xl font-bold leading-tight">
              Hello it's{" "}
              <span className="text-[#00D9FF] text-4xl lg:text-7xl">Me</span>
              {" "}
              <span className="text-white text-7xl lg:text-8xl">Ryan </span>
              <span className="text-[#00D9FF] text-7xl lg:text-8xl">Li</span>
            </h2>
            
            <p className="text-gray-300 text-lg leading-relaxed max-w-xl">
              And I'm a CS Master's student at Rice University aspiring to be an AI/ML engineer and software developer. 
            </p>
          </div>
          
          {/* Right Content - Profile Card */}
          <div className="flex justify-center lg:justify-start lg:pl-8">
            <div className="relative">
              {/* Glowing background */}
              <div className="absolute inset-0 bg-[#FFD700] rounded-full blur-3xl opacity-30 scale-110"></div>
              
              {/* Profile Card */}
              <div className="relative bg-[#2a2a2a] rounded-3xl p-16 border border-gray-700 max-w-sm">
                <div className="text-center">
                  {/* Profile Image with glow */}
                  <div className="relative mb-6">
                    <div className="absolute inset-0 bg-[#FFD700] rounded-full blur-lg opacity-50"></div>
                    <Image
                      src="/ryan_graduation.jpeg"
                      alt="Ryan Li"
                      className="relative rounded-full mx-auto border-4 border-[#FFD700] shadow-xl"
                      width={180}
                      height={180}
                      priority
                    />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-white mb-2">
                    RYAN LI
                  </h3>
                  
                  <div className="bg-gray-600 text-white px-4 py-1 rounded-full text-sm mb-4 inline-block">
                    CS STUDENT
                  </div>
                  
                  <div className="space-y-3 text-left">
                    <div className="text-gray-400 text-sm space-y-1">
                      <p><span className="text-white font-semibold">EMAIL:</span> rl182@rice.edu</p>
                      <p><span className="text-white font-semibold">Phone number:</span> +1 (346) 404-7839</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
      
      {/* Green accent elements */}
      <div className="absolute top-40 right-20 w-2 h-20 bg-[#00D9FF] opacity-60"></div>
      <div className="absolute bottom-40 left-10 w-4 h-4 bg-[#00D9FF] rounded-full animate-pulse"></div>
    </div>
  );
}
