// pages/api/summarize.ts

export const runtime = 'edge';

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
      const response = await axios.post('http://localhost:5000/summarize', { text });
      if (response.status === 200) {
        res.status(200).json({ summary: response.data.summary });
      } else {
        res.status(response.status).json({ error: 'Error summarizing text' });
      }
    } catch (error) {
      res.status(500).json({ error: 'Error summarizing text' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
