import React, { useState } from 'react';
import Navbar from './Navbar';
import './css/SharedImagePool.css';

const SharedImagePool = () => {
    const [showCreateGroupModal, setShowCreateGroupModal] = useState(false);
    const [showAddUserModal, setShowAddUserModal] = useState(false);
    const [groupName, setGroupName] = useState('');
    const [userId, setUserId] = useState('');
    const [showAddPermissionsModal, setShowAddPermissionsModal] = useState(false);
    const [permissions, setPermissions] = useState({ read: false, write: false, delete: false });
    const headers = {
        Authorization: `Bearer ${localStorage.getItem('token_payload')}`,
      };

    const createGroup = async () => {
        const formData = new FormData();
        formData.append('group_name', groupName);

        const response = await fetch('http://127.0.0.1:8000/shared_image_pool/create_group', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        if (!response.ok) {
            console.error('Error:', response.status, response.statusText);
            return;
        }

        const data = await response.json();
        console.log('Group created:', data);
    };
    const addUserToGroup = async () => {
        const formData = new FormData();
        formData.append('group_name', groupName);
        formData.append('user_id', userId);

        const response = await fetch('http://127.0.0.1:8000/shared_image_pool/add_user_to_group', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        const data = await response.json();

        if (data.message === 'You are not the owner of this group') {
            alert('You are not the owner of this group and cannot perform this action.');
            return;
        }

        if (!response.ok) {
            console.error('Error:', response.status, response.statusText);
            return;
        }

        console.log('User added to group:', data);
    };

    const addPermissionsForUser = async () => {
        const formData = new FormData();
        formData.append('group_name', groupName);
        formData.append('user_id', userId);
        formData.append('read', permissions.read);
        formData.append('write', permissions.write);
        formData.append('delete', permissions.delete);

        const response = await fetch('http://127.0.0.1:8000/shared_image_pool/add_permissions_to_group', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        const data = await response.json();

        if (data.message === 'You are not the owner of this group') {
            alert('You are not the owner of this group and cannot perform this action.');
            return;
        }

        if (!response.ok) {
            console.error('Error:', response.status, response.statusText);
            return;
        }

        console.log('Permissions added for user:', data);
    };

    const handleOpenCreateGroupModal = () => {
        setShowCreateGroupModal(true);
        setShowAddUserModal(false);
        setShowAddPermissionsModal(false);
    };

    const handleOpenAddUserModal = () => {
        setShowCreateGroupModal(false);
        setShowAddUserModal(true);
        setShowAddPermissionsModal(false);
    };

    const handleOpenAddPermissionsModal = () => {
        setShowCreateGroupModal(false);
        setShowAddUserModal(false);
        setShowAddPermissionsModal(true);
    };

    const handleCloseCreateGroupModal = () => {
        setShowCreateGroupModal(false);
    };


    const handleCloseAddUserModal = () => {
        setShowAddUserModal(false);
    };

    const handleGroupNameChange = (event) => {
        setGroupName(event.target.value);
    };

    const handleUserIdChange = (event) => {
        setUserId(event.target.value);
    };

    const handleCloseAddPermissionsModal = () => {
        setShowAddPermissionsModal(false);
    };

    const handlePermissionChange = (event) => {
        setPermissions({ ...permissions, [event.target.name]: event.target.checked });
    };
    return (
        <div>
            <Navbar />
            <div className="shared-image-pool">
                <div className="container">
                <h1>Shared Image Pool</h1>
                <button onClick={handleOpenCreateGroupModal}>Create Group</button>
                {showCreateGroupModal && (
                    <div className="modal">
                        <h2>Create Group</h2>
                        <input type="text" value={groupName} onChange={handleGroupNameChange} placeholder="Group Name" />
                        <button onClick={createGroup}>Submit</button>
                        <button onClick={handleCloseCreateGroupModal}>Close</button>
                    </div>
                )}
                <button onClick={handleOpenAddUserModal}>Add User to Group</button>
                {showAddUserModal && (
                    <div className="modal">
                        <h2>Add User to Group</h2>
                        <input type="text" value={groupName} onChange={handleGroupNameChange} placeholder="Group Name" />
                        <input type="text" value={userId} onChange={handleUserIdChange} placeholder="User ID" />
                        <button onClick={addUserToGroup}>Submit</button>
                        <button onClick={handleCloseAddUserModal}>Close</button>
                    </div>
                )}
               <button onClick={handleOpenAddPermissionsModal}>Add Permissions for User</button>
                {showAddPermissionsModal && (
                    <div className="modal">
                        <h2>Add Permissions for User</h2>
                        <input type="text" value={groupName} onChange={handleGroupNameChange} placeholder="Group Name" />
                        <input type="text" value={userId} onChange={handleUserIdChange} placeholder="User ID" />
                        <label>
                            <input type="checkbox" name="read" checked={permissions.read} onChange={handlePermissionChange} />
                            Read
                        </label>
                        <label>
                            <input type="checkbox" name="write" checked={permissions.write} onChange={handlePermissionChange} />
                            Write
                        </label>
                        <label>
                            <input type="checkbox" name="delete" checked={permissions.delete} onChange={handlePermissionChange} />
                            Delete
                        </label>
                        <button onClick={addPermissionsForUser}>Submit</button>
                        <button onClick={handleCloseAddPermissionsModal}>Close</button>
                    </div>
                )}
            </div>
        </div>
        </div>
    );
}

export default SharedImagePool;