import React, { useState } from 'react';
import Image from 'next/image';

interface ImageItem {
  url: string;
  prompt: string;
  timestamp: string;
  local_path?: string;
}

interface ImageBoardProps {
  images: ImageItem[];
  onDownload: (imagePath: string, fileName: string) => void;
}

const ImageBoard: React.FC<ImageBoardProps> = ({ images, onDownload }) => {
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {images.map((image: ImageItem, index: number) => (
          <div 
            key={index} 
            className="group border border-gray-700/50 rounded-xl overflow-hidden bg-gray-900/30 backdrop-blur-sm
                     transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/10"
          >
            <div className="relative w-full h-48 bg-gray-800/50 flex items-center justify-center group-hover:bg-gray-800/70 transition-colors">
              {image.url ? (
                <>
                  <Image
                    src={image.url.startsWith('http') ? image.url : `http://localhost:8000/${image.local_path?.replace('./', '')}`}
                    alt={image.prompt || 'Generated/Downloaded Image'}
                    layout="fill"
                    objectFit="cover"
                    className="cursor-zoom-in transition-transform duration-300 group-hover:scale-110"
                    onClick={() => setSelectedImage(index)}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                </>
              ) : (
                <span className="text-gray-400">No Image Preview</span>
              )}
            </div>
            <div className="p-4 space-y-2">
              <div className="min-h-[3rem]">
                <p className="text-sm text-gray-300 font-medium line-clamp-2 group-hover:line-clamp-none transition-all">
                  {image.prompt}
                </p>
              </div>
              <p className="text-xs text-gray-500">{image.timestamp}</p>
              {image.local_path && (
                <button
                  onClick={() => onDownload(image.local_path!, `image_${index}.png`)}
                  className="mt-3 w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg
                           hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 
                           focus:ring-purple-500/50 transition-all transform active:scale-95
                           shadow-lg shadow-purple-500/20"
                >
                  Download
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Modal for enlarged image view */}
      {selectedImage !== null && (
        <div 
          className="fixed inset-0 bg-black/90 backdrop-blur-xl z-50 flex items-center justify-center cursor-pointer"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative w-full max-w-4xl h-[80vh] p-4">
            <Image
              src={images[selectedImage].url.startsWith('http') 
                ? images[selectedImage].url 
                : `http://localhost:8000/${images[selectedImage].local_path?.replace('./', '')}`}
              alt={images[selectedImage].prompt || 'Enlarged Image'}
              layout="fill"
              objectFit="contain"
              className="rounded-lg"
            />
            <button
              className="absolute top-4 right-4 text-white bg-gray-800/50 rounded-full p-2 hover:bg-gray-700/50 transition-colors"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedImage(null);
              }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div className="absolute bottom-4 left-4 right-4 bg-gray-900/80 backdrop-blur-sm p-4 rounded-lg">
              <p className="text-white text-sm">{images[selectedImage].prompt}</p>
              <p className="text-gray-400 text-xs mt-1">{images[selectedImage].timestamp}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ImageBoard;
