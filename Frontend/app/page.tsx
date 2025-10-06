import Link from "next/link";
import Image from "next/image";

export default function Page() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0a] via-[#1a1a2e] to-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-600/20 via-transparent to-transparent"></div>
        
        <div className="max-w-7xl mx-auto px-8 lg:px-16 pt-32 pb-20">
          <div className="text-center space-y-8">
            {/* Logo */}
            <div className="flex justify-center mb-8">
              <Image
                src="/logo.png"
                alt="NextMile Logo"
                width={200}
                height={200}
                className="rounded-2xl shadow-2xl"
                priority
              />
            </div>

            {/* Main Heading */}
            <h1 className="text-6xl lg:text-8xl font-bold leading-tight">
              <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
                NextMile
              </span>
            </h1>
            
            <p className="text-2xl lg:text-3xl text-gray-300 font-light max-w-4xl mx-auto">
              Your AI-Powered Career Assistant 🚀
            </p>
            
            <p className="text-lg lg:text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
              An innovative open-source resume platform that helps job seekers stand out with 
              personal portfolio pages, interactive resume displays, and an AI-powered digital twin assistant.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap justify-center gap-4 pt-8">
              <Link
                href="/ryan"
                className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-8 py-4 rounded-full font-semibold text-lg hover:from-blue-600 hover:to-cyan-600 transition-all duration-300 shadow-lg"
              >
                Try Live Demo
              </Link>
              <a
                href="https://github.com/Ryanrc03/Nextmile"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 border border-gray-700 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-700 transition-all duration-300"
              >
                ⭐ Star on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-[#0f0f0f]">
        <div className="max-w-7xl mx-auto px-8 lg:px-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-center mb-16">
            ✨ Key Features
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Feature 1 */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-gray-700 hover:border-blue-500 transition-all duration-300 hover:transform hover:scale-105">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="text-xl font-bold mb-3">Personal Portfolio</h3>
              <p className="text-gray-400">
                Create a dynamic online presence that highlights your projects, skills, and unique personality.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-gray-700 hover:border-cyan-500 transition-all duration-300 hover:transform hover:scale-105">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-3">Interactive Resume</h3>
              <p className="text-gray-400">
                Present your experience in engaging, visually rich formats that captivate recruiters.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-gray-700 hover:border-teal-500 transition-all duration-300 hover:transform hover:scale-105">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-3">AI Digital Twin</h3>
              <p className="text-gray-400">
                Advanced RAG assistant provides personalized feedback and tailored career advice.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-gray-700 hover:border-purple-500 transition-all duration-300 hover:transform hover:scale-105">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold mb-3">Open Source</h3>
              <p className="text-gray-400">
                Transparent, continuously improving platform with flexibility and customization.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-8 lg:px-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-center mb-16">
            💻 Tech Stack
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-blue-400">Frontend</h4>
              <p className="text-gray-400">React, Next.js, Tailwind CSS</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-green-400">Backend</h4>
              <p className="text-gray-400">FastAPI (Python), Node.js</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-yellow-400">Database</h4>
              <p className="text-gray-400">MongoDB, ChromaDB</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-purple-400">AI/ML</h4>
              <p className="text-gray-400">LangChain, HuggingFace, Transformers</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-cyan-400">DevOps</h4>
              <p className="text-gray-400">Docker, Docker Compose</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
              <h4 className="font-bold text-lg mb-2 text-red-400">Deployment</h4>
              <p className="text-gray-400">AWS EC2, Nginx, SSL/TLS</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-900/20 to-cyan-900/20">
        <div className="max-w-4xl mx-auto px-8 text-center space-y-6">
          <h2 className="text-4xl lg:text-5xl font-bold">
            Ready to Stand Out?
          </h2>
          <p className="text-xl text-gray-300">
            Try the live demo or explore the open-source code on GitHub
          </p>
          <div className="flex flex-wrap justify-center gap-4 pt-4">
            <Link
              href="/ryan"
              className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-8 py-4 rounded-full font-semibold text-lg hover:from-blue-600 hover:to-cyan-600 transition-all duration-300 shadow-lg"
            >
              Try Live Demo
            </Link>
            <a
              href="https://github.com/Ryanrc03/Nextmile"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-800 border border-gray-700 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-700 transition-all duration-300"
            >
              ⭐ Star on GitHub
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
