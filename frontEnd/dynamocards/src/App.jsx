import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [youtubeLink, setYoutubeLink] = useState("");
  const [responseData, setResponseData] = useState(null);

  const handleLinkChange = (event) => {
    setYoutubeLink(event.target.value);
  };

  const sendLink = async () => {
    try {
      const response = await axios.post("http://localhost:8000/analyze_video", {
        youtube_link: youtubeLink,
      });
      setResponseData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="App">
      <h1>Youtube Link to Flash Cards Generator</h1>
      <input 
        type="text"
        placeholder="Paste Link here"
        value={youtubeLink}
        onChange={handleLinkChange}
      />
      <button onClick={sendLink}>Generate Flash Cards</button>
      {responseData && (
        <div>
          <h2>Response Data:</h2>
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
