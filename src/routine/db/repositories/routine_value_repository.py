from typing import List, Optional

from psycopg2.extras import Json
from routine.db.base import Repository
from routine.config.logger import logger
from routine.domain.models.routine_value import RoutineValue
from routine.domain.exceptions import RoutineNotFoundError

class RoutineValueRepository(Repository[RoutineValue]):
    
    def find_by_id(self, id: int) -> Optional[RoutineValue]:
        query = "SELECT * FROM routines_values WHERE id = %(id)s"
        results = self.db.execute_query(query, {'id': id})
        
        if not results:
            return None
        
        return RoutineValue.from_dict(results[0])
    
    def find_all(self) -> List[RoutineValue]:
        query = "SELECT * FROM routines_values ORDER BY created_at DESC"
        results = self.db.execute_query(query)
        return [RoutineValue.from_dict(row) for row in results]
    
    def get_routine_value_by_routine_id_and_date(self, routine_id: int, date) -> Optional[RoutineValue]:
        query = "SELECT * FROM routines_values WHERE routine_id = %(routine_id)s AND date = %(date)s"
        results = self.db.execute_query(query, {'routine_id': routine_id, 'date': date})
        
        if not results:
            return None
        
        return RoutineValue.from_dict(results[0])   

    def create(self, routine_value: RoutineValue) -> RoutineValue:
        command = """
            INSERT INTO routines_values (routine_id, value, date, created_at)
            VALUES (%(routine_id)s, %(value)s, %(date)s, %(created_at)s)
            RETURNING id
        """
        params = routine_value.to_dict()
        params['value'] = Json(params['value'])
        with self.db.transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, params)
                routine_value.id = cursor.fetchone()[0]

        logger.info(f"RoutineValue created with id {routine_value.id}")
        return routine_value

    def update(self, routine_value: RoutineValue) -> RoutineValue:
        command = """
            UPDATE routines_values
            SET routine_id = %(routine_id)s, value = %(value)s, date = %(date)s, updated_at = NOW()
            WHERE id = %(id)s
        """
        params = routine_value.to_dict()
        params['value'] = Json(params['value'])
        rows = self.db.execute_command(command, params)
        
        if rows == 0:
            raise RoutineNotFoundError(f"RoutineValue {routine_value.id} not found")
        
        return routine_value

    def delete(self, id: int) -> bool:
        command = "DELETE FROM routines_values WHERE id = %(id)s"
        rows = self.db.execute_command(command, {'id': id})
        logger.info(f"RoutineValue deleted with id {id}")
        return rows > 0