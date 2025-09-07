import type { Metadata } from "next";
import { experiences } from "./experience-data";

export const metadata: Metadata = {
  title: "Experiences",
  description: "Professional Experience and Projects",
};

export default function Projects() {
  return (
    <section>
      <h1 className="mb-8 text-2xl font-medium">Professional Experience</h1>
      <div>
        {experiences.map((experience) => (
          <div
            key={experience.id}
            className="flex flex-col space-y-1 mb-5"
          >
            <div className="w-full flex flex-col space-y-2">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
                <h2 className="text-black dark:text-white font-semibold">{experience.position}</h2>
                <span className="text-sm text-neutral-500 dark:text-neutral-400">{experience.company}</span>
              </div>
              <p className="text-neutral-600 dark:text-neutral-400 text-sm">
                {experience.description}
              </p>
              <p className="text-neutral-500 dark:text-neutral-500 text-xs">
                <strong>Duration:</strong> {experience.duration}
              </p>
              <p className="text-neutral-500 dark:text-neutral-500 text-xs">
                <strong>Location:</strong> {experience.location}
              </p>
              <ul className="text-neutral-600 dark:text-neutral-400 text-sm list-disc list-inside">
                {experience.achievements.map((achievement, idx) => (
                  <li key={idx}>{achievement}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
