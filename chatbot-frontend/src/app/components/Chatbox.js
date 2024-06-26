"use client";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";

Chatbox.propTypes = {
  chatType: PropTypes.string.isRequired,
};

function Chatbox({ chatType }) {
  /**
   *@description: Chatbox component
   */

  // Set initial message to display on page load

  const initialMessageSushi = {
    text: "Hello! I know everything about sushi restaurants! How can I help you?",
    sender: "bot",
  };

  const initialMessageParking = {
    text: "Hello! I know everything about parking! How can I help you?",
    sender: "bot",
  };

  // State of all sent messages
  const [messagesSushi, setMessagesSushi] = useState([initialMessageSushi]);
  const [messagesParking, setMessagesParking] = useState([
    initialMessageParking,
  ]);

  // State of newly typed in message
  const [newMessage, setNewMessage] = useState("");

  //State for loading response
  const [loading, setLoading] = useState(false);

  //Set ref for automatic scrolling
  const chatboxRef = useRef();

  useEffect(() => {
    //Scroll to bottom of chatbox when new messages are added
    chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
  }, [messagesSushi, messagesParking]);

  const fetchResponse = async (userMessage) => {
    /**
     * @description:
     *  Get response for user message from the backend
     */

    // Set loading state to true
    setLoading(true);
    const endpoint =
      chatType === "sushi"
        ? "http://localhost:5000/sushi_chat"
        : "http://localhost:5000/parking_chat";

    // Fetch response from the chatbot server
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: userMessage, history: null }), // history thing might be too complicated
      credentials: "include", // Include cookies with the request
    });
    const data = await response.json();

    // Set loading state to false
    setLoading(false);

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
      if (chatType === "sushi")
        setMessagesSushi((prevMessages) => [...prevMessages, userMessage]);
      else setMessagesParking((prevMessages) => [...prevMessages, userMessage]);

      // Clear the input field
      setNewMessage("");

      // Get response from fetchResponse
      const getBotResponse = async () => {
        try {
          const botResponse = await fetchResponse(newMessage);
          const botMessage = { text: botResponse, sender: "bot" };
          if (chatType === "sushi") {
            setMessagesSushi((prevMessages) => [...prevMessages, botMessage]);
          } else
            setMessagesParking((prevMessages) => [...prevMessages, botMessage]);
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
        {chatType === "sushi"
          ? messagesSushi.map((msg, index) => (
              <div
                key={index}
                className={`mb-2 p-4 ${
                  msg.sender === "user" ? "text-right" : "text-left"
                } animate-fade-in`}
              >
                <span
                  className={`inline-block md:px-4 px-2 md:py-2 py-1 rounded md:text-lg lg:text-xl ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-300"
                  }`}
                >
                  {msg.text}
                </span>
              </div>
            ))
          : messagesParking.map((msg, index) => (
              <div
                key={index}
                className={`mb-2 p-4 ${
                  msg.sender === "user" ? "text-right" : "text-left"
                } animate-fade-in`}
              >
                <span
                  className={`inline-block md:px-4 px-2 md:py-2 py-1 rounded md:text-lg lg:text-xl ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-300"
                  }`}
                >
                  {msg.text}
                </span>
              </div>
            ))}
        {loading && (
          <div className="animate-fade-in text-left mb-2 p-4">
            <span className="inline-block md:px-4 px-2 md:py-2 py-1 rounded md:text-lg lg:text-xl md:w-32 w-28 bg-gray-300 typing-animation">
              Thinking
            </span>
          </div>
        )}
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
