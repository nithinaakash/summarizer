import { useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPizzaSlice } from '@fortawesome/free-solid-svg-icons';

const Home = () => {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/api/summarize', { text: inputText });
      if (response.status === 200) {
        setSummary(response.data.summary);
      } else {
        setError('Error summarizing text');
      }
    } catch (error) {
      console.error('Error summarizing text:', error);
      setError('Error summarizing text');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-center bg-black bg-opacity-60 p-10 rounded-xl shadow-xl backdrop-blur-sm w-full max-w-6xl h-auto">
      <h1 className="text-3xl text-white mb-5">Text Summarizer</h1>
      <div className={`flex ${summary ? 'flex-row' : 'flex-col'} items-center justify-center w-full transition-all duration-500`}>
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
          {loading ? <FontAwesomeIcon icon={faPizzaSlice} spin /> : 'Summarize'}
        </button>
        {summary && (
          <div className="ml-5 bg-white bg-opacity-10 p-5 rounded-lg shadow-md w-full transition-all duration-500 overflow-y-auto max-h-36">
            <h2 className="text-2xl text-white mb-3">Summary</h2>
            <p className="text-lg text-white">{summary}</p>
          </div>
        )}
      </div>
      {error && (
        <div className="mt-5 text-red-500 text-lg">
          {error}
        </div>
      )}
      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <FontAwesomeIcon icon={faPizzaSlice} size="4x" spin />
        </div>
      )}
    </div>
  );
};

export default Home;
