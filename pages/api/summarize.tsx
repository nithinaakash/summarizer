import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { text } = req.body;
    try {
      const response = await axios.post('http://localhost:5000/summarize', { text });
      res.status(200).json({ summary: response.data.summary });
    } catch (error) {
      res.status(500).json({ error: 'Error summarizing text' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
