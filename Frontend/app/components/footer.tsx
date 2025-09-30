"use client";

import React from "react";
import {
  FaXTwitter,
  FaGithub,
  FaInstagram,
  FaRss,
  FaLinkedinIn,
} from "react-icons/fa6";
import { TbMailFilled } from "react-icons/tb";
import { metaData, socialLinks } from "app/lib/config";

const YEAR = new Date().getFullYear();

function SocialLink({ href, icon: Icon }) {
  return (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="w-10 h-10 bg-[#1a1a1a] rounded-full flex items-center justify-center hover:bg-[#00ff88] hover:text-black transition-all duration-300"
    >
      <Icon />
    </a>
  );
}

function SocialLinks() {
  return (
    <div className="flex gap-4 justify-center lg:justify-start">
      <SocialLink href={socialLinks.twitter} icon={FaXTwitter} />
      <SocialLink href={socialLinks.github} icon={FaGithub} />
      <SocialLink href={socialLinks.instagram} icon={FaInstagram} />
      <SocialLink href={socialLinks.linkedin} icon={FaLinkedinIn} />
      <SocialLink href={socialLinks.email} icon={TbMailFilled} />
      <a 
        href="/rss.xml" 
        target="_self"
        className="w-10 h-10 bg-[#1a1a1a] rounded-full flex items-center justify-center hover:bg-[#00ff88] hover:text-black transition-all duration-300"
      >
        <FaRss />
      </a>
    </div>
  );
}

export default function Footer() {
  return (
    <footer className="bg-[#1a1a1a] border-t border-gray-800 py-12 px-8 lg:px-16">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col lg:flex-row justify-between items-center space-y-6 lg:space-y-0">
          
          {/* Personal Information */}
          <div className="text-center lg:text-left">
            <h3 className="text-xl font-bold text-white mb-2">Personal Information</h3>
            <div className="space-y-1 text-gray-400">
              <p><strong className="text-white">MOBILE NO:</strong> +1 (346) 404-7839</p>
              <p><strong className="text-white">INSTAGRAM:</strong> Ryanrc20003</p>
              <p><strong className="text-white">ADDRESS:</strong> Houston, TX</p>
              <p><strong className="text-white">EMAIL ID:</strong> rl182@rice.edu</p>
            </div>
          </div>
          
          {/* Social Links */}
          <div className="text-center">
            <SocialLinks />
            <div className="mt-4 text-gray-400 text-sm">
              © {YEAR} {" "}
              <a
                className="text-[#00ff88] hover:underline"
                href={socialLinks.twitter}
                target="_blank"
                rel="noopener noreferrer"
              >
                {metaData.title}
              </a>
              {". All rights reserved."}
            </div>
          </div>
          
        </div>
      </div>
    </footer>
  );
}
