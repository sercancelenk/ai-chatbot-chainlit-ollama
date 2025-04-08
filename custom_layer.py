# from chainlit.element import ElementDict
# from chainlit.step import StepDict
# from chainlit.logger import logger
# from typing import Optional, Dict, List
# import json
# from chainlit.data.sql_alchemy import SQLAlchemyDataLayer as OriginalSQLAlchemyDataLayer
# import chainlit as cl


# class CustomSQLAlchemyDataLayer(OriginalSQLAlchemyDataLayer):
#     async def create_step(self, step_dict: StepDict):
#         if self.show_logger:
#             logger.info(f"SQLAlchemy: create_step, step_id={step_dict.get('id')}")
#         step_dict["showInput"] = (
#             str(step_dict.get("showInput", "")).lower()
#             if "showInput" in step_dict
#             else None
#         )
#         step_dict["disableFeedback"] = step_dict.get("disableFeedback", False)  # Add this line
#         parameters = {
#             key: value
#             for key, value in step_dict.items()
#             if value is not None and not (isinstance(value, dict) and not value)
#         }
#         parameters["metadata"] = json.dumps(step_dict.get("metadata", {}))
#         parameters["generation"] = json.dumps(step_dict.get("generation", {}))
#         columns = ", ".join(f'"{key}"' for key in parameters.keys())
#         values = ", ".join(f":{key}" for key in parameters.keys())
#         updates = ", ".join(
#             f'"{key}" = :{key}' for key in parameters.keys() if key != "id"
#         )
#         query = f"""
#             INSERT INTO steps ({columns})
#             VALUES ({values})
#             ON CONFLICT (id) DO UPDATE
#             SET {updates};
#         """
#         await self.execute_sql(query=query, parameters=parameters)

#     async def update_thread(
#         self,
#         thread_id: Optional[str] = None,
#         name: Optional[str] = None,
#         user_id: Optional[str] = None,
#         metadata: Optional[Dict] = None,
#         tags: Optional[List[str]] = None,
#     ):
#         if self.show_logger:
#             logger.info(f"SQLAlchemy: update_thread, thread_id={thread_id}")
        
#         user = cl.user_session.get("user")
#         if not user:
#             raise ValueError("User not found in session")
        
#         user_identifier = user.identifier
        
#         data = {
#             "createdAt": await self.get_current_timestamp(),
#             "name": name,
#             "userId": user_id or user.id,
#             "userIdentifier": user_identifier,
#             "tags": tags,
#             "metadata": json.dumps(metadata) if metadata else None,
#         }
#         if thread_id:
#             data["id"] = thread_id

#         parameters = {key: value for key, value in data.items() if value is not None}
#         columns = ", ".join(f'"{key}"' for key in parameters.keys())
#         values = ", ".join(f":{key}" for key in parameters.keys())
        
#         if thread_id:
#             updates = ", ".join(f'"{key}" = EXCLUDED."{key}"' for key in parameters.keys() if key != "id")
#             query = f"""
#                 INSERT INTO threads ({columns})
#                 VALUES ({values})
#                 ON CONFLICT ("id") DO UPDATE
#                 SET {updates}
#                 RETURNING id;
#             """
#         else:
#             query = f"""
#                 INSERT INTO threads ({columns})
#                 VALUES ({values})
#                 RETURNING id;
#             """
        
#         result = await self.execute_sql(query=query, parameters=parameters)
#         if result and isinstance(result, list) and len(result) > 0:
#             return result[0]['id']
#         else:
#             raise ValueError("Failed to create or update thread")

#     async def get_element(self, element_id: str) -> Optional[ElementDict]:
#         if self.show_logger:
#             logger.info(f"CustomSQLAlchemy: get_element, element_id={element_id}")
#         query = """
#             SELECT * FROM elements
#             WHERE "id" = :element_id
#         """
#         result = await self.execute_sql(query=query, parameters={"element_id": element_id})
#         if isinstance(result, list) and result:
#             element_data = result[0]
#             return ElementDict(
#                 id=element_data["id"],
#                 threadId=element_data["threadId"],
#                 type=element_data["type"],
#                 url=element_data.get("url"),
#                 name=element_data["name"],
#                 display=element_data["display"],
#                 forId=element_data.get("forId"),
#             )
#         return None
