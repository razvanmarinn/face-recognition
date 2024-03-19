import React, { useState, useEffect, useRef } from 'react';
import './css/Profile.css'; 
import Navbar from './Navbar';

const Profile = () => {
    const [email, setEmail] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [age, setAge] = useState(0);
    const userId = localStorage.getItem('userId');
    const [profilePic, setProfilePic] = useState("default.jpg");
    const fileInput = useRef();
    const faceAuthInput = useRef();

    const handleFaceAuthClick = () => {
        faceAuthInput.current.click();
    }

    const handleFaceAuthChange = async (e) => {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('image', file);
        formData.append('face_auth', true);
        const headers = {
            Authorization: `Bearer ${localStorage.getItem('token_payload')}`,
        };
    
        try {
            const response = await fetch('http://127.0.0.1:8000/face_recognition/add_face', {
                method: 'POST',
                headers: headers,
                body: formData,
            });
    
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onloadend = () => {
            setProfilePic(reader.result);
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            setProfilePic("default.jpg");
        }
    }

    const handleClick = () => {
        fileInput.current.click();
    }

    useEffect(() => {
        fetch(`http://127.0.0.1:8001/user_details/get_user_details?user_id=${userId}`, {method:'GET'})
        .then(response => response.json())
        .then(data => {
            setEmail(data.email);
            setFirstName(data.first_name);
            setLastName(data.last_name);
            setAge(data.age);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }, [userId]); 

    const handleBlur = () => {
        if (!email.includes('@') || !(email.includes('yahoo.com') || email.includes('gmail.com'))) {
            alert('Invalid email. Email should include @ and domain should be yahoo.com or gmail.com');
            return;
        }

        fetch(`http://127.0.0.1:8001/user_details/edit_user_details?user_id=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                age: age,
                email: email
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
    }


    return (
        <div className="profile-page">
            <Navbar /> {}
            <div className="content-container">
                <div className="container">
                    <h1>Profile Page</h1>
                    {/* <div className="profile-picture">
                        <img src={profilePic} alt="Profile" />
                        <input type="file" ref={fileInput} onChange={handleImageChange} style={{display: 'none'}} />
                        <button onClick={handleClick}>Change Picture</button>
                    </div> */}
                    <div className="face-auth">
                        <input type="file" ref={faceAuthInput} onChange={handleFaceAuthChange} style={{display: 'none'}} />
                        <button onClick={handleFaceAuthClick}>Add Pictures for Face Auth</button>
                    </div>
                    <div className="profile-info">
                        <p><strong>Email:</strong> <span contentEditable="true" onBlur={e => setEmail(e.target.textContent)}>{email}</span></p>
                        <p><strong>Name:</strong> <span contentEditable="true" onBlur={e => setFirstName(e.target.textContent)}>{firstName}</span></p>
                        <p><strong>Surname:</strong> <span contentEditable="true" onBlur={e => setLastName(e.target.textContent)}>{lastName}</span></p>
                        <p><strong>Age:</strong> <span contentEditable="true" onBlur={e => setAge(e.target.textContent)}>{age}</span></p>
                    </div>
                    <button onClick={handleBlur}>Save Changes</button>
                </div>
            </div>
        </div>
    );
};

export default Profile;