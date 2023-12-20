import React, { useState, useRef, useEffect } from 'react';

const MainPage = () => {
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

              console.log('Server Response:', response.text());
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
    <div>
      <h2>Welcome to the Home Page!</h2>
      <div>
        <input
          type="text"
          value={text}
          onChange={handleTextChange}
          placeholder="Enter text..."
        />
        {stream && (
          <div>
            <video ref={videoRef} autoPlay playsInline />
            <button onClick={takePicture}>Take Picture</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainPage;
