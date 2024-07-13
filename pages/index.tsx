import { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await axios.post('/api/summarize', { text: inputText });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error summarizing text:', error);
    }
  };

  return (
    <div>
      <h1>Text Summarizer</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Paste or type your text here..."
      />
      <button onClick={handleSubmit}>Summarize</button>
      {summary && (
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default Home;
