"use client";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Image from "next/image";
import React, { useEffect, useRef, useState } from "react";

function Chatbox() {
  /**
   *@description: Chatbox component
   */

  // Set initial message to display on page load
  const initialMessage = {
    text: "Wie kann ich Ihnen behilflich sein?",
    sender: "bot",
  };
  // State of all sent messages
  const [messages, setMessages] = useState([initialMessage]);
  // State of newly typed in message
  const [newMessage, setNewMessage] = useState("");

  //Set ref for automatic scrolling
  const chatboxRef = useRef();

  useEffect(() => {
    //Scroll to bottom of chatbox when new messages are added
    chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
  }, [messages]);

  const fetchResponse = async (userMessage) => {
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: userMessage, history: null }), // history thing might be too complicated
    });
    const data = await response.json();
    return data.response;
  };

  const handleSendMessage = async () => {
    /**
     * @description:
     *  Send-message handler. Adds the sent message to the history
     *  of messages and requests the chatbot response.
     */
    if (newMessage.trim() !== "") {
      // Add the user's message to the chat history
      const userMessage = { text: newMessage, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      // Clear the input field
      setNewMessage("");

      // Get response from fetchResponse
      const getBotResponse = async () => {
        try {
          const botResponse = await fetchResponse(newMessage);
          const botMessage = { text: botResponse, sender: "bot" };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
          console.error("Error fetching bot response:", error);
        }
      };

      getBotResponse();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Prevents a newline character in the input
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col justify-between md:p-10 p-4 md:h-full h-screen bg-opacity-30 backdrop-blur-xl lg:w-1/2 w-full bg-gray-800 shadow-2xl rounded-2xl">
      <div
        ref={chatboxRef}
        className="md:p-6 p-2 rounded shadow-md w-full h-screen max-h-[65vh] md:max-h-screen overflow-y-auto mb-4"
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-2 p-4 ${
              msg.sender === "user" ? "text-right" : "text-left"
            } animate-fade-in`}
          >
            <span
              className={`inline-block md:px-4 px-2 md:py-2 py-1 rounded md:text-lg lg:text-xl ${
                msg.sender === "user" ? "bg-blue-600 text-white" : "bg-gray-300"
              }`}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex items-center w-full px-4 gap-4">
        <textarea
          rows="1"
          className="flex-1 border rounded p-2 bg-gray-800 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
          placeholder="Type your message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="flex justify-center items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded"
          onClick={handleSendMessage}
        >
          <FontAwesomeIcon icon={faPaperPlane} />
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbox;
