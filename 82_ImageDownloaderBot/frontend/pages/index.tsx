import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Image from 'next/image';
import axios from 'axios';

interface ImageItem {
  url: string;
  local_path?: string;
  prompt?: string;
  timestamp: string;
}

const Home: React.FC = () => {
  // Add a loading toast notification state
  const [toast, setToast] = useState<{
    show: boolean;
    message: string;
    type: 'success' | 'error' | 'loading';
  }>({ show: false, message: '', type: 'loading' });
  const [prompt, setPrompt] = useState<string>('');
  const [imageUrl, setImageUrl] = useState<string>('');
  const [selectedModel, setSelectedModel] = useState<'gemini' | 'openai'>('gemini');
  const [images, setImages] = useState<ImageItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // In a real application, you might fetch previously saved images here
  }, []);

  const handleGenerateImage = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/generate', {
        prompt,
        model: selectedModel,
      });
      const newImages = response.data.images.map((img: any) => ({
        url: img.url,
        local_path: img.local_path,
        prompt: prompt,
        timestamp: new Date().toLocaleString(),
      }));
      setImages((prevImages) => [...prevImages, ...newImages]);
      setPrompt('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate image.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadImageUrl = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/download', {
        url: imageUrl,
      });
      const newImage: ImageItem = {
        url: imageUrl,
        local_path: response.data.local_path,
        prompt: 'Downloaded from URL',
        timestamp: new Date().toLocaleString(),
      };
      setImages((prevImages) => [...prevImages, newImage]);
      setImageUrl('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to download image from URL.');
    } finally {
      setLoading(false);
    }
  };

  const downloadImageLocally = (imagePath: string, fileName: string) => {
    // This is a simplified approach. In a production Next.js app,
    // you'd typically have a backend endpoint to serve these files securely.
    // For local development, you might directly link to the backend's static serve directory
    // or trigger a download via a blob.
    // For now, we'll just open the image in a new tab if it's a direct URL.
    if (imagePath.startsWith('http')) {
      window.open(imagePath, '_blank');
    } else {
      // Assuming backend serves static files from /downloaded_images
      window.open(`http://localhost:8000/${imagePath.replace('./', '')}`, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-8">
      <Head>
        <title>ImageDownloaderBot</title>
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </Head>

      <main className="container mx-auto bg-gray-800/50 backdrop-blur-xl p-8 rounded-2xl shadow-2xl border border-gray-700">
        {/* Toast Notification */}
        {toast.show && (
          <div className={`fixed top-4 right-4 p-4 rounded-lg shadow-lg transition-all transform ${
            toast.show ? 'translate-y-0 opacity-100' : '-translate-y-4 opacity-0'
          } ${
            toast.type === 'success' ? 'bg-green-500' :
            toast.type === 'error' ? 'bg-red-500' : 'bg-blue-500'
          }`}>
            <p className="text-white">{toast.message}</p>
          </div>
        )}
        <h1 className="text-5xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 mb-4">
          ImageDownloaderBot
        </h1>
        <p className="text-center text-gray-400 mb-8">Generate and download stunning images with AI or from URLs</p>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-6 py-4 rounded-xl relative mb-6 backdrop-blur-sm" role="alert">
            <strong className="font-bold">Error:</strong>
            <span className="block sm:inline ml-2">{error}</span>
          </div>
        )}

        {/* Prompt-based Image Generation */}
        <section className="mb-8 p-6 border border-gray-700/50 rounded-xl bg-gray-800/30 backdrop-blur-sm transition-all hover:bg-gray-800/50">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Generate Image from Prompt</h2>
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <input
              type="text"
              className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your image prompt (e.g., 'A futuristic city')"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <select
              className="p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value as 'gemini' | 'openai')}
            >
              <option value="gemini">Gemini</option>
              <option value="openai">OpenAI (DALL-E)</option>
            </select>
            <button
              onClick={handleGenerateImage}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              disabled={loading || !prompt}
            >
              {loading ? 'Generating...' : 'Generate Image'}
            </button>
          </div>
        </section>

        {/* URL-based Image Downloading */}
        <section className="mb-8 p-6 border rounded-lg bg-gray-50">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Download Image from URL</h2>
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <input
              type="text"
              className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Paste public image URL (e.g., https://unsplash.com/photos/...) "
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
            />
            <button
              onClick={handleDownloadImageUrl}
              className="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50"
              disabled={loading || !imageUrl}
            >
              {loading ? 'Downloading...' : 'Download Image'}
            </button>
          </div>
        </section>

        {/* Image Board */}
        <section className="p-6 border rounded-lg bg-gray-50">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Image Board</h2>
          {images.length === 0 && !loading && (
            <p className="text-gray-600 text-center">No images yet. Generate or download some!</p>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {images.map((image, index) => (
              <div key={index} className="border rounded-lg overflow-hidden shadow-lg bg-white">
                <div className="relative w-full h-48 bg-gray-200 flex items-center justify-center">
                  {image.url ? (
                    <Image
                      src={image.url.startsWith('http') ? image.url : `http://localhost:8000/${image.local_path?.replace('./', '')}`}
                      alt={image.prompt || 'Generated/Downloaded Image'}
                      layout="fill"
                      objectFit="contain"
                      className="cursor-pointer"
                      onClick={() => window.open(image.url.startsWith('http') ? image.url : `http://localhost:8000/${image.local_path?.replace('./', '')}`, '_blank')}
                    />
                  ) : (
                    <span className="text-gray-500">No Image Preview</span>
                  )}
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-800 font-medium mb-2">Prompt: {image.prompt}</p>
                  <p className="text-xs text-gray-500">{image.timestamp}</p>
                  {image.local_path && (
                    <button
                      onClick={() => downloadImageLocally(image.local_path!, `image_${index}.png`)}
                      className="mt-3 w-full px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                    >
                      Download
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;
