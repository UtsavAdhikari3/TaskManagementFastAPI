from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.role import Role


DEFAULT_ROLES = ["ADMIN", "MANAGER", "USER"]


def seed_roles(db: Session):
    for role_name in DEFAULT_ROLES:
        existing_role = db.query(Role).filter(Role.name == role_name).first()

        if not existing_role:
            role = Role(name=role_name)
            db.add(role)

    db.commit()


def main():
    db = SessionLocal()
    try:
        seed_roles(db)
        print("Roles seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()