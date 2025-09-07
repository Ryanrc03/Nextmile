import Image from "next/image";
import { socialLinks } from "./lib/config";

export default function Page() {
  return (
    <section>
      <a href={socialLinks.twitter} target="_blank">
        <Image
          src="/Ryan_hippocampus.jpg"
          alt="Profile photo"
          className="rounded-full bg-gray-100 block lg:mt-5 mt-0 lg:mb-5 mb-10 mx-auto sm:float-right sm:ml-5 sm:mb-5 hover:grayscale-0"
          unoptimized
          width={160}
          height={160}
          priority
        />
      </a>
      <h1 className="mb-8 text-2xl font-medium">Ryan`s Portfolio</h1>
      <div className="prose prose-neutral dark:prose-invert">
        <p>
          My name is Ryan Li, I am a Computer Science Master's student at the Rice University.
        </p>
        <p>
          Welcome to My Portfolio!
        </p>
         <p>
          I was born in Guangzhou, China, and completed my undergraduate degree in Computer Science at Hong Kong Baptist University.
        </p>
        <p>
          I am seeking AI/ML, Software, and Data internship opportunities in the United States for summer 2026.
        </p>
      </div>
    </section>
  );
}
