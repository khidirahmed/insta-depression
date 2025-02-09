import React from 'react';
import styled from 'styled-components';

const Button = () => {
    return (
        <StyledWrapper>
            <button>
                <span>Search X</span>
            </button>
        </StyledWrapper>
    );
}

const StyledWrapper = styled.div`
    button {
        background: #fff;
        border: none;
        padding: 15px 30px; /* Increased padding */
        display: inline-block;
        font-size: 20px; /* Increased font size */
        font-weight: 700; /* Make text bolder */
        width: 170px; /* Increased button width */
        height: 50px; /* Increased button height */
        text-transform: uppercase;
        cursor: pointer;
        transform: skew(-21deg);
    }

  span {
    display: inline-block;
    transform: skew(21deg);
  }

  button::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    right: 100%;
    left: 0;
    background: rgb(20, 20, 20);
    opacity: 0;
    z-index: -1;
    transition: all 0.5s;
  }

  button:hover {
    color: #fff;
  }

  button:hover::before {
    left: 0;
    right: 0;
    opacity: 1;
  }`;

export default Button;
