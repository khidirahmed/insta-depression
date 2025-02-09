import React, { useState } from "react";
import styled from "styled-components";

const ProgressBar3 = () => {
    const [progress, setProgress] = useState(0);

    const increaseProgress = () => {
        setProgress((prev) => (prev >= 100 ? 100 : prev + 10)); // Increase by 10%
    };

    return (
        <Container>
            <p>Anxiety</p>
            <Bar>
                <Fill style={{ width: `${progress}%` }} />
            </Bar>
            <Percentage>{progress}%</Percentage>
        </Container>
    );
};

export default ProgressBar3;

// Styled Components
const Container = styled.div`
  text-align: center;
  margin-top: 15px;
`;

const Bar = styled.div`
    width: 300px;
    height: 20px;
    background: #ffffff;
    border-radius: 10px;
    overflow: hidden;
    margin: 10px auto;
    border: 2px solid black;
`;

const Fill = styled.div`
  height: 100%;
  background: #4caf50;
  transition: width 0.3s ease-in-out;
`;

const Percentage = styled.p`
  font-size: 18px;
  margin: 5px 0;
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background: #4caf50;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;

  &:hover {
    background: #45a049;
  }
`;