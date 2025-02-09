import React, { useState } from "react";
import styled from "styled-components";

const ThoughtContainer = () => {
    const [thought, setThought] = useState("Click the button to get an AI thought...");

    const fetchThought = () => {
        // Simulate AI response (Replace with actual AI API call)
        const thoughts = [
            "Thinking deeply about the universe...",
            "Analyzing patterns in data...",
            "Exploring the mysteries of human consciousness...",
            "Optimizing algorithms for better efficiency...",
            "Learning from previous experiences..."
        ];
        setThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
    };

    return (
        <Container>
            <Title>AI Reasoning</Title>
            <Box>{thought}</Box>
        </Container>
    );
};

export default ThoughtContainer;

// Styled Components
const Container = styled.div`
  text-align: center;
  margin-top: 30px;
`;

const Title = styled.h2`
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
`;

const Box = styled.div`
  width: 500px;
  min-height: 150px;
  background: #f4f4f4;
  border: 3px solid #333; /* Thick border */
  border-radius: 10px;
  padding: 15px;
  font-size: 18px;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
`;

const Button = styled.button`
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    background: #84e087;
    color: white;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 15px;

    &:hover {
        background: #84e087;
    }
`;