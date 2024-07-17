This project provides a text summarizer application that leverages a Flask backend with a BART/RAG model for text summarization and a Next.js frontend for user interaction.


CloudFare Pages Deployment: https://summarizer-lhe.pages.dev/ <br>
Vercel Deployment: https://ragsummarizer.vercel.app/

Currently, the project returns the input text in the summary box because the backend deployment in the free tier does not have enough memory/storage space to download the required libraries. However, it works perfectly on local setups.

Demo on localserver:


## Getting Started


Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

# Flask RAG Summarizer

Flask that uses the `facebook/rag-token-base` model from Hugging Face's Transformers library to summarize text. The application provides a RESTful API endpoint for summarizing text.

## Features

- Summarize input text using the RAG model.
- RESTful API endpoint for text summarization.

## Requirements

- Python 3.8+
- `flask`
- `torch`
- `transformers`
- `datasets`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/flask-rag-summarizer.git
   cd flask-rag-summarizer


## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Backend Setup (Flask)

### Requirements

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/text-summarizer.git
    cd text-summarizer/backend/vercel
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Running the Flask Server

1. Start the Flask server:

    ```sh
    python app.py
    ```

   The server will start on `http://0.0.0.0:5000`.

## Frontend Setup (Next.js)

### Requirements

- Node.js 14 or higher
- npm (Node package manager)

### Installation

1. Navigate to the frontend directory:

    ```sh
    cd ../frontend
    ```

2. Install the required packages:

    ```sh
    npm install
    ```

### Running the Next.js Application

1. Start the Next.js development server:

    ```sh
    npm run dev
    ```

   The application will be available at `http://localhost:3000`.

## Deployment

### Vercel Deployment

To deploy the Next.js frontend on Vercel:

1. Install the Vercel CLI:

    ```sh
    npm install -g vercel
    ```

2. Run the deployment command:

    ```sh
    vercel
    ```

   Follow the prompts to deploy your application.

To deploy the Flask backend on Vercel:

1. Ensure your `requirements.txt` is up-to-date with all dependencies.
2. Create a `vercel.json` configuration file in the backend directory:

    ```json
    {
      "version": 2,
      "builds": [
        {
          "src": "app.py",
          "use": "@vercel/python"
        }
      ],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "app.py"
        }
      ]
    }
    ```

3. Run the deployment command from the backend directory:

    ```sh
    vercel
    ```

## Usage

1. Open the Next.js application in your browser.
2. Enter the text you want to summarize in the provided text area.
3. Click the "Summarize" button.
4. The summarized text will be displayed on the right side of the input.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License.
