from typing import List


class SharedImagePool:
    """
SharedImagePool class is used to create a shared image pool.
Need to create a shared image pool in the database, and keep it updated when users add permisions, face names or users
to the pool.
    """
    owner_id = None
    image_pool_name = None
    face_names = []
    members = []
    permissions = []

    def __init__(self, owner_id: int, image_pool_name: str, face_names: List[str], members: List[int] = None,
                 permissions: List[dict] = None):
        self.owner_id = owner_id
        self.image_pool_name = image_pool_name
        self.face_names = face_names
        self.members = members
        self.permissions = permissions

    def add_user_to_pool(self, user_id: int):
        if user_id not in self.members:
            self.members.append(user_id)
        else:
            print("User already in pool")

    def add_face_name_to_pool(self, user_id, face_name: str):
        # If two or more users add the same face name, the face name will be added to the pool only once but the images
        # from the users will be added to the pool to that name
        if face_name not in self.face_names:
            self.face_names.append({"user_id": user_id, "face_name": face_name})
        else:
            print("Face name already in pool")

    def init_permisions(self):
        for member in self.members:
            if member in self.permissions['user_id']:
                continue
            self.permissions.append({"user_id": member, "read": True, "write": False, "delete": False})

    def grant_permisions(self, current_user_id, target_user_id, write: bool, delete: bool):
        for permission in self.permissions:
            if permission["user_id"] == target_user_id and current_user_id == self.owner_id:
                permission["write"] = write
                permission["delete"] = delete
                break
        else:
            print("User not in pool")

