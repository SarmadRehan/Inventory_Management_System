class User:
   
      def __init__(self, user_id: int, name: str, username: str, password: str, role: enumerate) -> None:
        self.name = name
        self.user_id = user_id
        self.username = username
        self.password =  password
        self.role = role

      def __str__(self) -> str:
        return f"User: {self.name} (Role: {self.role})"

      def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, name='{self.name}', username='{self.username}', role='{self.role}')"
