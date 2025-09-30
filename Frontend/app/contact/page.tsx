"use client";

import { useState } from "react";

export default function ContactPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    mobNo: '',
    emailId: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSubmitStatus('success');
        setFormData({
          firstName: '',
          lastName: '',
          mobNo: '',
          emailId: '',
          message: ''
        });
      } else {
        setSubmitStatus('error');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl lg:text-6xl font-bold mb-6">
              CONTACT <span className="text-[#00D9FF]">ME</span>:
            </h1>
            <div className="w-24 h-1 bg-[#00D9FF] mx-auto mb-8"></div>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Have a project in mind or want to collaborate? I'd love to hear from you. 
              Send me a message and I'll get back to you as soon as possible.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Form */}
      <section className="py-10 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto">
          <div className="bg-[#1a1a1a] rounded-xl p-8 lg:p-12 border border-gray-700">
            
            {/* Status Messages */}
            {submitStatus === 'success' && (
              <div className="mb-8 p-4 bg-green-900/30 border border-green-700 rounded-lg">
                <p className="text-green-400 text-center">
                  ✅ Message sent successfully! I'll get back to you soon.
                </p>
              </div>
            )}
            
            {submitStatus === 'error' && (
              <div className="mb-8 p-4 bg-red-900/30 border border-red-700 rounded-lg">
                <p className="text-red-400 text-center">
                  ❌ Failed to send message. Please try again or contact me directly.
                </p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* First Row - Name Fields */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleChange}
                    placeholder="First Name:"
                    required
                    className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors"
                  />
                </div>
                <div>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleChange}
                    placeholder="Last Name:"
                    required
                    className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors"
                  />
                </div>
              </div>

              {/* Second Row - Contact Fields */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <input
                    type="tel"
                    name="mobNo"
                    value={formData.mobNo}
                    onChange={handleChange}
                    placeholder="mob.no:"
                    className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors"
                  />
                </div>
                <div>
                  <input
                    type="email"
                    name="emailId"
                    value={formData.emailId}
                    onChange={handleChange}
                    placeholder="Email Id:"
                    required
                    className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors"
                  />
                </div>
              </div>

              {/* Message Field */}
              <div>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="MESSAGE :

Type your message here"
                  required
                  rows={8}
                  className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-[#00D9FF] transition-colors resize-none"
                />
              </div>

              {/* Submit Button */}
              <div className="text-center pt-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-[#00D9FF] hover:bg-[#00B8CC] disabled:bg-gray-600 disabled:cursor-not-allowed text-black px-12 py-4 rounded-lg text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl"
                >
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* Contact Information */}
      <section className="py-20 px-8 lg:px-16 bg-[#1a1a1a]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Get In <span className="text-[#00D9FF]">Touch</span>
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Email */}
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="w-16 h-16 bg-[#00D9FF] rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Email</h3>
              <p className="text-gray-400 mb-2">rl182@rice.edu</p>
              <p className="text-gray-400">ryanrc230107@gmail.com</p>
            </div>

            {/* Phone */}
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="w-16 h-16 bg-[#00D9FF] rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Phone</h3>
              <p className="text-gray-400">+1 (346) 404-7839</p>
            </div>

            {/* Location */}
            <div className="bg-[#2a2a2a] p-8 rounded-xl border border-gray-700 text-center hover:border-[#00D9FF] transition-all duration-300">
              <div className="w-16 h-16 bg-[#00D9FF] rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Location</h3>
              <p className="text-gray-400">Houston, TX</p>
              <p className="text-gray-400">United States</p>
            </div>
          </div>
        </div>
      </section>

      {/* Social Links */}
      <section className="py-20 px-8 lg:px-16">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12">
            Connect With <span className="text-[#00D9FF]">Me</span>
          </h2>
          
          <div className="flex justify-center space-x-6">
            <a href="mailto:rl182@rice.edu" className="w-16 h-16 bg-[#1a1a1a] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#00D9FF] hover:text-black hover:border-[#00D9FF] transition-all duration-300">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
            </a>
            <a href="#" className="w-16 h-16 bg-[#1a1a1a] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#00D9FF] hover:text-black hover:border-[#00D9FF] transition-all duration-300">
              <span className="text-xl">🐦</span>
            </a>
            <a href="#" className="w-16 h-16 bg-[#1a1a1a] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#00D9FF] hover:text-black hover:border-[#00D9FF] transition-all duration-300">
              <span className="text-xl">💼</span>
            </a>
            <a href="#" className="w-16 h-16 bg-[#1a1a1a] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#00D9FF] hover:text-black hover:border-[#00D9FF] transition-all duration-300">
              <span className="text-xl">📱</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}