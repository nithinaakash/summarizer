export const config = {
  runtime: 'edge',  // Set the runtime to edge
};

import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

type Data = {
  summary?: string;
  error?: string;
};

export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  if (req.method === 'POST') {
    const { text } = req.body;
    try {
      const response = await axios.post('https://ef595f2a.summarizer-lhe.pages.dev/api/summarize', { text });  // Replace with your backend URL
      res.status(200).json({ summary: response.data.summary });
    } catch (error: any) {  // Ensure 'error' is typed as 'any'
      if (axios.isAxiosError(error) && error.response) {
        res.status(error.response.status).json({ error: error.response.data.error || 'Error summarizing text' });
      } else {
        res.status(500).json({ error: 'Error summarizing text' });
      }
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
