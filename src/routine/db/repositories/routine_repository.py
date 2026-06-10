import json
from typing import List, Optional

from routine.db.base import Repository
from routine.config.logger import logger
from routine.domain.models.routine import Routine
from routine.domain.exceptions import RoutineNotFoundError


class RoutineRepository(Repository[Routine]):
    def find_by_id(self, id: int) -> Optional[Routine]:
        query = "SELECT * FROM routines WHERE id = %(id)s"
        results = self.db.execute_query(query, {"id": id})

        if not results:
            return None

        return Routine.from_dict(results[0])

    def find_by_user_id_and_name(self, user_id: str, name: str) -> Optional[Routine]:
        query = "SELECT * FROM routines WHERE user_id = %(user_id)s AND name = %(name)s"
        results = self.db.execute_query(query, {"user_id": user_id, "name": name})

        if not results:
            return None

        return Routine.from_dict(results[0])

    def find_all(self) -> List[Routine]:
        query = "SELECT * FROM routines ORDER BY created_at DESC"
        results = self.db.execute_query(query)
        return [Routine.from_dict(row) for row in results]

    def find_all_by_user_id(self, user_id: str) -> List[Routine]:
        query = "SELECT * FROM routines WHERE user_id = %(user_id)s ORDER BY created_at DESC"
        results = self.db.execute_query(query, {"user_id": user_id})
        return [Routine.from_dict(row) for row in results]

    def _to_db_params(self, routine: Routine) -> dict:
        params = routine.to_dict()
        params["multiselect_options"] = json.dumps(params["multiselect_options"])
        params["tags"] = json.dumps(params["tags"])
        return params

    def create(self, routine: Routine) -> Routine:
        command = """
            INSERT INTO routines (user_id, name, type, multiselect_options, tags, description, created_at)
            VALUES (%(user_id)s, %(name)s, %(type)s, %(multiselect_options)s, %(tags)s, %(description)s, %(created_at)s)
            RETURNING id
        """
        with self.db.transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, self._to_db_params(routine))
                routine.id = cursor.fetchone()[0]

        logger.info(f"Routine created with id {routine.id}")
        return routine

    def update(self, routine: Routine) -> Routine:
        command = """
            UPDATE routines
            SET name = %(name)s, type = %(type)s, multiselect_options = %(multiselect_options)s, tags = %(tags)s, description = %(description)s, updated_at = NOW()
            WHERE id = %(id)s
        """
        rows = self.db.execute_command(command, self._to_db_params(routine))

        if rows == 0:
            raise RoutineNotFoundError(f"Routine {routine.id} not found")

        return routine

    def delete(self, id: int) -> bool:
        command = "DELETE FROM routines WHERE id = %(id)s"
        rows = self.db.execute_command(command, {"id": id})
        logger.info(f"Routine deleted with id {id}")
        return rows > 0
