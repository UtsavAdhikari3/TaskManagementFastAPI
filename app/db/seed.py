from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password


DEFAULT_ROLES = ["ADMIN", "MANAGER", "USER"]


DEFAULT_USERS = [
    {
        "email": "admin@gmail.com",
        "full_name": "Admin User",
        "password": "Password123",
        "role": "ADMIN",
    },
    {
        "email": "manager@gmail.com",
        "full_name": "Manager User",
        "password": "Password123",
        "role": "MANAGER",
    },
    {
        "email": "normal@gmail.com",
        "full_name": "Normal User",
        "password": "Password123",
        "role": "USER",
    },
]


def seed_roles(db: Session):
    for role_name in DEFAULT_ROLES:
        existing_role = db.query(Role).filter(Role.name == role_name).first()

        if not existing_role:
            role = Role(name=role_name)
            db.add(role)

    db.commit()


def seed_users(db: Session):
    for user_data in DEFAULT_USERS:
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()

        if existing_user:
            continue

        role = db.query(Role).filter(Role.name == user_data["role"]).first()

        if not role:
            raise Exception(f"Role {user_data['role']} not found. Seed roles first.")

        user = User(
            email=user_data["email"],
            full_name=user_data["full_name"],
            hashed_password=hash_password(user_data["password"]),
            role_id=role.id,
            is_active=True,
        )

        db.add(user)

    db.commit()


def main():
    db = SessionLocal()

    try:
        seed_roles(db)
        seed_users(db)
        print("Roles and users seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()