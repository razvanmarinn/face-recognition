import React, { useState, useRef, useEffect, useCallback} from 'react';
import './css/Recognize.css';
import Navbar from './Navbar';

const Recognize = () => {
  const [stream, setStream] = useState(null);
  const [sipCheck, setSipCheck] = useState(false); 
  const [loading, setLoading] = useState(false);
  const [emotionCheck, setEmotionCheck] = useState(false);
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
  }, []); 
  
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
            const formData = new FormData();
            formData.append('image', new Blob([imageBytes]));
  
            const headers = {
              Authorization: `Bearer ${localStorage.getItem('token_payload')}`,
            };
  
            try {
              let response;
              if (sipCheck) { // New block of code for Shared Image pools
                response = await fetch('http://127.0.0.1:8000/face_recognition/identify?sip=true', {
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
                  const name = jsonResponse[0].details.name;
                  const sharedImagePoolName = jsonResponse[0].details.pool_name;
            
                  if (!isNaN(confidence) && confidence >= 70) {
                    alert('The person in the image is ' + name + ' with a confidence of ' + confidence + '% from Shared Image Pool ' + sharedImagePoolName);
                    if (emotionCheck) { //
                      const emotionFormData = new FormData();
                      emotionFormData.append('image', new Blob([imageBytes]));
                      const emotionResponse = await fetch('http://127.0.0.1:8000/face_emotion_recognition/predict-emotion/', {
                        method: 'POST',
                        headers: headers,
                        body: emotionFormData
                      });
                      if (emotionResponse.ok) {
                        const emotionJsonResponse = await emotionResponse.json();
                        console.log('Emotion JSON Response:', emotionJsonResponse);
                        alert(`Predicted Emotion: ${emotionJsonResponse.predicted_emotion}`);
                      } else {
                        throw new Error('Emotion prediction request failed!');
                      }
                    }
                  } else {
                    alert('Recognition Confidence Below 70');
                  }
                } else {
                  alert('Incomplete or Unexpected JSON Structure');
                }
              }

              } else {
                response = await fetch('http://127.0.0.1:8000/face_recognition/identify', {
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
                    const name = jsonResponse[0].details.name;
              
                    if (!isNaN(confidence) && confidence >= 70) {
                      alert('The person in the image is ' + name + ' with a confidence of ' + confidence + '%');
                      if (emotionCheck) { // Only call the emotion recognition API if the checkbox is checked
                        const emotionFormData = new FormData();
                        emotionFormData.append('image', new Blob([imageBytes]));
                        const emotionResponse = await fetch('http://127.0.0.1:8000/face_emotion_recognition/predict-emotion/', {
                          method: 'POST',
                          headers: headers,
                          body: emotionFormData
                        });
                        if (emotionResponse.ok) {
                          const emotionJsonResponse = await emotionResponse.json();
                          console.log('Emotion JSON Response:', emotionJsonResponse);
                          alert(`Predicted Emotion: ${emotionJsonResponse.predicted_emotion}`);
                        } else {
                          throw new Error('Emotion prediction request failed!');
                        }
                      }
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
              }
              }
              catch (error) {
                console.error('Error sending data:', error);
              }
  
            setLoading(false);
            if (stream) {
              stream.getTracks().forEach(track => track.stop());
            }
            startCamera(); 
          };
        }
      }, 'image/png');
    }
  };


  const handleEmotionCheckChange = (event) => { 
    setEmotionCheck(event.target.checked);
  };

  const handleSipCheckChange = (event) => { 
    setSipCheck(event.target.checked); // New handler for Shared Image pools
  };

  return (
    <div>
      <Navbar />
      <div className="main-container">
        <div className="inner-container">
          <h2 className="header-text">Recognition Flow!</h2>
          <div className="input-section">
           
            <input
              type="checkbox"
              checked={emotionCheck}
              onChange={handleEmotionCheckChange}
              className="emotion-check-input"
            />
            <label htmlFor="emotion-check-input">Check for Emotion Recognition</label>
            <input
              type="checkbox"
              checked={sipCheck} 
              onChange={handleSipCheckChange} 
              className="sip-check-input"
            />
            <label htmlFor="sip-check-input">Check from Shared Image pools</label>
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
