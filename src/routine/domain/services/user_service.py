from routine.db.repositories.user_repository import UserRepository
from routine.domain.models.user import User
from routine.domain.exceptions import UserAlreadyExistsError, AuthenticationError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(
        self,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        password_confirm: str,
    ) -> User:
        if (
            not firstname
            or not lastname
            or not email
            or not password
            or not password_confirm
        ):
            raise ValueError("Tous les champs sont obligatoires")

        if password != password_confirm:
            raise ValueError("Les mots de passe ne correspondent pas")

        if "@" not in email:
            raise ValueError("Email invalide")

        if self.repo.find_by_email(email):
            raise UserAlreadyExistsError("Un compte existe déjà avec cet email")

        user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password_hash="",  # sera défini ci-dessous
        )
        user.set_password(password)
        return self.repo.create(user)

    def authenticate(self, email: str, password: str) -> User:
        if not email or not password:
            raise ValueError("Email et mot de passe requis")

        user = self.repo.find_by_email(email)
        if not user or not user.check_password(password):
            raise AuthenticationError("Email ou mot de passe invalide")

        return user
