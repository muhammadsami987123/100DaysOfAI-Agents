import React, { useState } from 'react';

interface URLInputProps {
  onDownload: (url: string) => void;
  loading: boolean;
}

const URLInput: React.FC<URLInputProps> = ({ onDownload, loading }) => {
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isValidUrl, setIsValidUrl] = useState<boolean>(true);

  const validateUrl = (url: string): boolean => {
    try {
      new URL(url);
      return url.match(/\.(jpg|jpeg|png|webp|gif)$/i) !== null;
    } catch {
      return false;
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const url = e.target.value;
    setImageUrl(url);
    setIsValidUrl(url === '' || validateUrl(url));
  };

  const handleSubmit = () => {
    if (imageUrl.trim() && validateUrl(imageUrl)) {
      onDownload(imageUrl);
      setImageUrl('');
      setIsValidUrl(true);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-grow relative">
          <input
            type="text"
            className={`w-full p-4 bg-gray-900/50 border rounded-xl text-white placeholder-gray-400 
                     focus:outline-none focus:ring-2 transition-all ${
                       isValidUrl 
                         ? 'border-gray-700 focus:ring-green-500/50 focus:border-green-500/50' 
                         : 'border-red-500/50 focus:ring-red-500/50 focus:border-red-500/50'
                     }`}
            placeholder="Paste public image URL (e.g., https://example.com/image.jpg)"
            value={imageUrl}
            onChange={handleUrlChange}
            onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => { if (e.key === 'Enter') handleSubmit(); }}
          />
          {!isValidUrl && imageUrl && (
            <span className="absolute -bottom-6 left-2 text-sm text-red-400">
              Please enter a valid image URL (jpg, jpeg, png, webp, gif)
            </span>
          )}
        </div>
        
        <button
          onClick={handleSubmit}
          className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl
                   hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 
                   focus:ring-green-500/50 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all transform hover:scale-105 active:scale-95 min-w-[160px]
                   font-semibold shadow-lg hover:shadow-green-500/20"
          disabled={loading || !imageUrl.trim() || !isValidUrl}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Downloading...
            </span>
          ) : 'Download Image'}
        </button>
      </div>
      
      {imageUrl && isValidUrl && (
        <div className="text-sm text-gray-400 px-2">
          <p>URL: <span className="text-green-400 font-medium truncate inline-block max-w-md align-bottom">{imageUrl}</span></p>
        </div>
      )}
    </div>
  );
};

export default URLInput;
