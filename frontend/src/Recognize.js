import React, { useState, useRef, useEffect, useCallback} from 'react';
import './css/Recognize.css';
import Navbar from './Navbar';

const Recognize = () => {
  const [stream, setStream] = useState(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const videoRef = useRef();

  const startCamera = useCallback(async () => {
    setLoading(true);
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.play();
      }
    } catch (error) {
      console.error('Error accessing the camera:', error);
    }
    setLoading(false);
  }, []); // Removed 'stream' from the dependency array
  
  useEffect(() => {
    startCamera();
  }, [startCamera]);
  

  const takePicture = async () => {
    setLoading(true);
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
              } 

              else {
                throw new Error('Request failed!');
              }
            } catch (error) {
              console.error('Error sending data:', error);
            }

            setLoading(false);
            if (stream) {
              stream.getTracks().forEach(track => track.stop());
            }
            startCamera(); // Restart the camera here
          };
        }
      }, 'image/png');
    }
  };

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div>
      <Navbar />
      <div className="main-container">
        <div className="inner-container">
          <h2 className="header-text">Recognition Flow!</h2>
          <div className="input-section">
            <input
              type="text"
              value={text}
              onChange={handleTextChange}
              placeholder="Enter text..."
              className="text-input"
            />
            {!loading && stream && (
              <div className="video-section">
                <video ref={videoRef} autoPlay playsInline className="video-element" />
                <button onClick={takePicture} className="picture-button">
                  Take Picture
                </button>
              </div>
            )}
          </div>
          {loading && <div className="loading-spinner"></div>}
        </div>
      </div>
    </div>
  );
  };
  
  export default Recognize;
