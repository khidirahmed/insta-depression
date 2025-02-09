import React from 'react'
import "./Home.css"
import Input from "./input"
import Button from "./sexy-button";
import ProgressBar from "./progress-bar";
import ProgressBar2 from "./progress-bar2";
import ProgressBar3 from "./progress-bar3";
import ThoughtContainer from "./reasonContainer";

function Home() {
  return (
      <div className="homeContainer">
          <header className="header">
              <div className="logo">X-pression</div>
          </header>
          <h1>Analyze your emotions with AI, enter a username to get started.</h1>
          <Input/>
          <Button/>
          <ProgressBar/>
          <ProgressBar2/>
          <ProgressBar3/>
          <ThoughtContainer/>
      </div>
  )
}

export default Home
