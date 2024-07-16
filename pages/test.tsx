import { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/summarize', { text: inputText });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error summarizing text:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-600">
      <h1 className="text-3xl text-white mb-5">Text Summarizer</h1>
      <div className={`flex ${summary ? 'flex-row' : 'flex-col'} items-center justify-center w-full max-w-6xl transition-all duration-500`}>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste or type your text here..."
          className={`w-full ${summary ? 'h-36' : 'h-36 mb-5'} p-2 rounded-lg border-none text-lg bg-white bg-opacity-10 text-white resize-none shadow-md transition-all duration-500`}
        />
        <button
          onClick={handleSubmit}
          className={`py-2 px-5 rounded-md bg-blue-600 text-white text-lg cursor-pointer transition duration-300 ease-in-out hover:bg-blue-800 ${summary ? 'mx-5' : ''}`}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Summarize'}
        </button>
        {summary && (
          <div className="ml-5 bg-white bg-opacity-10 p-5 rounded-lg shadow-md w-full transition-all duration-500 overflow-y-auto max-h-36">
            <h2 className="text-2xl text-white mb-3">Summary</h2>
            <p className="text-lg text-white">{summary}</p>
          </div>
        )}
      </div>
      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="loader"></div>
        </div>
      )}
    </div>
  );
};

export default Home;
