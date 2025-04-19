import React, { useState } from 'react';

function App() {
  const [data, setData] = useState("");
  const [message, setMessage] = useState("");

  const sendDataToCloud = async () => {
    const response = await fetch("http://127.0.0.1:5000/store-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data }),
    });
    const result = await response.json();
    setMessage(result.message);
  };

  return (
    <div>
      <h1>Armazenamento de Dados na Nuvem</h1>
      <input
        type="text"
        placeholder="Digite os dados"
        value={data}
        onChange={(e) => setData(e.target.value)}
      />
      <button onClick={sendDataToCloud}>Enviar para a Nuvem</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;