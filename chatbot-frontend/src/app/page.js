"use client";
import Chatbox from "./components/Chatbox";
import { useState } from "react";

export default function Home() {
  //Tab state
  const [activeTab, setActiveTab] = useState("sushi");

  return (
    <main className="home-container">
      <div className="flex flex-col md:justify-center items-center md:w-1/4 xl:px-20">
        <h1 className="md:text-4xl text-2xl text-white font-semibold text-center">
          Chatbot
        </h1>
        <div className="flex border-b border-gray-200 mb-4">
          <button
            className={`py-2 px-4 text-sm font-medium text-center ${
              activeTab === "sushi"
                ? "border-b-2 border-blue-400 text-blue-400"
                : "text-gray-300 hover:text-gray-900"
            }`}
            onClick={() => setActiveTab("sushi")}
          >
            Sushi Info
          </button>
          <button
            className={`py-2 px-4 text-sm font-medium text-center ${
              activeTab === "parking"
                ? "border-b-2 border-blue-400 text-blue-400"
                : "text-gray-300 hover:text-white"
            }`}
            onClick={() => setActiveTab("parking")}
          >
            Parking Info
          </button>
        </div>
        <div className="lg:absolute lg:block top-20 left-28 hidden"></div>
      </div>
      <Chatbox chatType={activeTab} />
    </main>
  );
}
