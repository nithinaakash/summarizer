// import { NextApiRequest, NextApiResponse } from 'next';
// import axios from 'axios';

// type Data = {
//   summary?: string;
//   error?: string;
// };

// export const config = {
//   runtime: 'edge',  // Set the runtime to edge
// };

// export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
//   if (req.method === 'POST') {
//     const { text } = req.body;
//     console.log("Sending data:", { text });  // Debug statement
//     try {
//       const response = await axios.post('http://localhost:5000/summarize', { text });  // Local Flask backend URL
//       res.status(200).json({ summary: response.data.summary });
//     } catch (error: any) {  // Ensure 'error' is typed as 'any'
//       console.error("Error:", error);  // Debug statement
//       if (axios.isAxiosError(error) && error.response) {
//         res.status(error.response.status || 500).json({ error: error.response.data.error || 'Error summarizing text' });
//       } else {
//         res.status(500).json({ error: 'Error summarizing text' });
//       }
//     }
//   } else {
//     res.status(405).json({ error: 'Method not allowed' });
//   }
// }

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