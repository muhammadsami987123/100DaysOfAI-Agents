import React, { useState } from 'react';

interface PromptInputProps {
  onGenerate: (prompt: string, model: 'gemini' | 'openai') => void;
  loading: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ onGenerate, loading }) => {
  const [prompt, setPrompt] = useState<string>('');
  const [selectedModel, setSelectedModel] = useState<'gemini' | 'openai'>('gemini');
  const [charCount, setCharCount] = useState<number>(0);
  const MAX_CHARS = 1000;

  const handlePromptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newPrompt = e.target.value;
    if (newPrompt.length <= MAX_CHARS) {
      setPrompt(newPrompt);
      setCharCount(newPrompt.length);
    }
  };

  const handleSubmit = () => {
    if (prompt.trim()) {
      onGenerate(prompt, selectedModel);
      setPrompt('');
      setCharCount(0);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-grow relative">
          <input
            type="text"
            className="w-full p-4 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-400 
                     focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
            placeholder="Enter your image prompt (e.g., 'A futuristic city')"
            value={prompt}
            onChange={handlePromptChange}
            onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => { if (e.key === 'Enter') handleSubmit(); }}
          />
          <span className={`absolute right-3 bottom-3 text-sm ${
            charCount > MAX_CHARS * 0.9 ? 'text-red-400' : 'text-gray-400'
          }`}>
            {charCount}/{MAX_CHARS}
          </span>
        </div>
        
        <select
          className="p-4 bg-gray-900/50 border border-gray-700 rounded-xl text-white 
                   focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all
                   appearance-none cursor-pointer min-w-[180px]"
          value={selectedModel}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedModel(e.target.value as 'gemini' | 'openai')}
        >
          <option value="gemini" className="bg-gray-900">Gemini</option>
          <option value="openai" className="bg-gray-900">OpenAI (DALL-E)</option>
        </select>
        
        <button
          onClick={handleSubmit}
          className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl
                   hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 
                   focus:ring-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all transform hover:scale-105 active:scale-95 min-w-[160px]
                   font-semibold shadow-lg hover:shadow-purple-500/20"
          disabled={loading || !prompt.trim()}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating...
            </span>
          ) : 'Generate Image'}
        </button>
      </div>
      
      {prompt && (
        <div className="text-sm text-gray-400 px-2">
          <p>Model: <span className="text-purple-400 font-medium">{selectedModel === 'gemini' ? 'Google Gemini' : 'OpenAI DALL-E'}</span></p>
        </div>
      )}
    </div>
  );
};

export default PromptInput;
