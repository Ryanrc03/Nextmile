import ExperienceClient from "../components/ExperienceClient";

export const metadata = {
  title: "Experience",
  description: "Ryan's Internship and Research Experience",
};

export default function Experience() {
  return (
    <section>
      <h1 className="mb-8 text-2xl font-medium">Internship Experience</h1>
      <ExperienceClient />
    </section>
  );
}
