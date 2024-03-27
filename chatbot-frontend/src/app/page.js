import Image from "next/image";
import Chatbox from "./components/Chatbox";

export default function Home() {
  return (
    <main className="home-container">
      <div className="flex sm:flex-row flex-col md:justify-center items-center md:w-1/4 xl:px-20">
        <h1 className="md:text-4xl text-2xl text-white font-semibold text-center">
          FAQ-Bot
        </h1>
        <div className="lg:absolute lg:block top-20 left-28 hidden"></div>
      </div>
      <Chatbox />
    </main>
  );
}
