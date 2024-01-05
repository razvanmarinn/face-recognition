import React, { useState, useRef, useEffect } from 'react';
import './Recognize.css';

const Recognize = () => {
  const [stream, setStream] = useState(null);
  const [text, setText] = useState('');
  const videoRef = useRef();

  useEffect(() => {
    const startCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (error) {
        console.error('Error accessing the camera:', error);
      }
    };

    startCamera();
  }, []);

  const takePicture = async () => {
    if (videoRef.current) {
      const video = videoRef.current;
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(async (blob) => {
        if (blob) {
          const reader = new FileReader();
          reader.readAsArrayBuffer(blob);
          reader.onloadend = async () => {
            const imageBytes = reader.result;
            const textData = text;
            const formData = new FormData();
            formData.append('image', new Blob([imageBytes]));
            formData.append('face_name', textData);


            const headers = {
                Authorization: `Bearer ${localStorage.getItem('token_payload')}`,
              };
            

            try {
              const response = await fetch('http://127.0.0.1:8000/face_recognition/recognize', {
                method: 'POST',
                headers: headers,
                body: formData
              });
              
              if (response.ok) {
                try {
                  const jsonResponse = await response.json();
                  console.log('JSON Response:', jsonResponse); 
              
                  if (jsonResponse && jsonResponse.length > 0 && jsonResponse[0].details && jsonResponse[0].details.confidence_level) {
                    const confidenceStr = jsonResponse[0].details.confidence_level;
                    const confidence = parseFloat(confidenceStr.replace('%', ''));
              
                    if (!isNaN(confidence) && confidence >= 70) {
                      alert('Recognition Successful');
                    } else {
                      alert('Recognition Confidence Below 70');
                    }
                  } else {
                    alert('Incomplete or Unexpected JSON Structure');
                  }
                } catch (error) {
                  console.error('Error parsing JSON response:', error);
                }
              } else {
                throw new Error('Request failed!');
              }
              
            } catch (error) {
              console.error('Error sending data:', error);
            }
          };
        }
      }, 'image/png');
    }
  };

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="main-container">
      <h2>Recognition flow!</h2>
      <div className="input-section">
        <input
          type="text"
          value={text}
          onChange={handleTextChange}
          placeholder="Enter text..."
          className="text-input" 
        />
        {stream && (
          <div className="video-section">
            <video ref={videoRef} autoPlay playsInline className="video-element" />
            <button onClick={takePicture} className="picture-button">Take Picture</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recognize;
