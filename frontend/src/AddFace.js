import React, { useState } from 'react';
import './css/AddFace.css';
import Navbar from './Navbar';

const AddFace = () => {
    const [name, setName] = useState('');
    const [image, setImage] = useState(null);
    const [isChecked, setIsChecked] = useState(false);
    const [sharedImagePool, setSharedImagePool] = useState('');

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    const callApi = async () => {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('image', image);
        const headers = {
            Authorization: `Bearer ${localStorage.getItem('token_payload')}`,
        };

        try {
            let response;
            if (isChecked) {
                // TODO: To look at the code for adding face to shared image pool
                formData.append('group_name', sharedImagePool);
                response = await fetch('http://127.0.0.1:8000/shared_image_pool/add_face_to_group', {
                    method: 'POST',
                    headers: headers,
                    body: formData,
                });
            } else {
                response = await fetch('http://127.0.0.1:8000/face_recognition/add_face', {
                    method: 'POST',
                    headers: headers,
                    body: formData,
                });
            }

            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
          <Navbar />
          <div className="add-face">
            <div className='container'>
              <h2>Welcome to the AddFace Page!</h2>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter name" />
              <input type="file" onChange={handleImageChange} />
              <div>
                <label>
                  <input type="checkbox" checked={isChecked} onChange={(e) => setIsChecked(e.target.checked)} />
                  Add face to shared image pool
                </label>
                {isChecked && <input type="text" value={sharedImagePool} onChange={(e) => setSharedImagePool(e.target.value)} placeholder="Enter shared image pool" />}
              </div>
              <button onClick={callApi}>Submit</button>
            </div>
          </div>
        </div>
      );
}

export default AddFace;