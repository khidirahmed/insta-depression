import React, { useState } from "react";
import "./Home.css";
import Button from "./sexy-button";
import ProgressBar from "./progress-bar";
import ThoughtContainer from "./reasonContainer";

function Home() {
    const [mood, setMood] = useState({
        Depression: 0,
        Anxiety: 0,
        Happiness: 0,
        Explanation: ""
    });

    const handleAnalyze = async () => {
        // Open the Spotify login in a new tab
        const loginTab = window.open("http://127.0.0.1:5000/", "_blank");

        // Wait a few seconds for the user to log in, then fetch the analysis data
        setTimeout(async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/analyze", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include", // Include cookies for session handling
                });

                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Update the mood state with the analyzed data
                setMood({
                    Depression: data.Depression,
                    Anxiety: data.Anxiety,
                    Happiness: data.Happiness,
                    Explanation: data.Explanation,
                });
            } catch (error) {
                console.error("Error fetching analysis data:", error);
            }
        }, 5000); // Adjust the timeout based on how long it takes users to log in
    };
    return (
        <div className="homeContainer">
            <header className="header">
                <div className="logo">Expressify</div>
            </header>
            <h1>Analyze your emotions from Spotify utilizing AI. Log in to get started.</h1>
            <Button onClick={handleAnalyze}>Connect Spotify</Button>
            <ProgressBar percentage={mood.Depression} label="Depression" />
            <ProgressBar percentage={mood.Anxiety} label="Anxiety" />
            <ProgressBar percentage={mood.Happiness} label="Happiness" />
            <ThoughtContainer text={mood.Explanation} />
        </div>
    );
}

export default Home;