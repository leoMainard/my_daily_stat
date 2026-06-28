from routine.config.logger import logger
from typing import List, Optional
from routine.db.base import Repository
from routine.domain.models.user import User
from routine.domain.exceptions import UserNotFoundError


class UserRepository(Repository[User]):
    def find_by_id(self, id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = self.db.execute_query(query, {"id": id})

        if not results:
            return None

        return User.from_dict(results[0])

    def find_all(self) -> List[User]:
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = self.db.execute_query(query)
        return [User.from_dict(row) for row in results]

    def find_by_email(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = self.db.execute_query(query, {"email": email})
        return User.from_dict(results[0]) if results else None

    def create(self, user: User) -> User:
        command = """
            INSERT INTO users (firstname, lastname, email, password_hash, role, created_at)
            VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password_hash)s, %(role)s, %(created_at)s)
            RETURNING id
        """
        with self.db.transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, user.to_dict())
                user.id = cursor.fetchone()[0]

        logger.info(f"User created with id {user.id}")
        return user

    def update(self, user: User) -> User:
        command = """
            UPDATE users 
            SET firstname = %(firstname)s, lastname = %(lastname)s, email = %(email)s, role = %(role)s, updated_at = NOW()
            WHERE id = %(id)s
        """
        rows = self.db.execute_command(command, user.to_dict())

        if rows == 0:
            raise UserNotFoundError(f"User {user.id} not found")

        return user

    def delete(self, id: int) -> bool:
        command = "DELETE FROM users WHERE id = %(id)s"
        rows = self.db.execute_command(command, {"id": id})
        logger.info(f"User deleted with id {id}")
        return rows > 0
