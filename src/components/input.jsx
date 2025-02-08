import { useState } from "react";

function Input() {
    const [username, setUsername] = useState("");

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <label htmlFor="username" style={{ fontSize: "30px", fontWeight: "bold" }}>
                Enter Username:
            </label>
            <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Type your username..."
                style={{
                    marginLeft: "10px",
                    padding: "8px",
                    fontSize: "16px",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                }}
            />
            <p style={{ marginTop: "10px", fontSize: "18px" }}>
                X(FKA Twitter) Username @<strong>{username}</strong>
            </p>
        </div>
    );
}

export default Input;