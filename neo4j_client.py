from neo4j import GraphDatabase
from models import UserNode, UserRelationship
class Neo4jClient:
    def __init__(self, URI, user, password):
        self.URI = URI
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(self.URI, auth=(self.user, self.password))
        try:
            self._set_db_constraints()
        except:
            pass
    
    def _set_db_constraints(self):
        def _set_constraints(tx):
            tx.run("CREATE CONSTRAINT ON(u:USER) ASSERT u.uid IS UNIQUE")
        with self.driver.session() as session:
            session.write_transaction(_set_constraints)

    
    def get_follower_count(self, uid: str) -> int:
        def _get_follower_count(tx, uid: str):
            result = tx.run(CypherQueryGenerator.get_followers_count_query(uid))
            return result.values()[0][0]
        with self.driver.session() as session:
            return session.write_transaction(_get_follower_count, uid)
            
    
    def get_following_count(self, uid: str) -> int:
        def _get_following_count(tx, uid: str):
            result = tx.run(CypherQueryGenerator.get_following_count_query(uid))
            return result.values()[0][0]
        with self.driver.session() as session:
            return session.write_transaction(_get_following_count, uid)
    
    def follow_user(self, userRelationship: UserRelationship):
        def _follow_user(tx, userRelationship: UserRelationship):
            tx.run(CypherQueryGenerator.get_create_relationship_query(userRelationship))
        with self.driver.session() as session:
            session.write_transaction(_follow_user, userRelationship)
    
    def unfollow_user(self, userRelationship: UserRelationship):
        def _unfollow_user(tx, userRelationship: UserRelationship):
            tx.run(CypherQueryGenerator.get_delete_relationship_query(userRelationship))
        with self.driver.session() as session:
            return session.write_transaction(_unfollow_user, userRelationship)
    
    def create_user(self, userNode: UserNode):
        def _create_user(tx, userNode: UserNode):
            result = tx.run(CypherQueryGenerator.get_create_node_query(userNode))
            return result
        with self.driver.session() as session:
            result =  session.write_transaction(_create_user, userNode)


    def delete_user(self, userNode: UserNode):
        def _delete_user(tx, userNode: UserNode):
            tx.run(CypherQueryGenerator.get_delete_node_query(userNode))
        with self.driver.session() as session:
            return session.write_transaction(_delete_user, userNode)
    
    def get_follow_suggestions(self, uid: str):
        def _get_follow_suggestions(tx, uid: str):
            result = tx.run(CypherQueryGenerator.get_follow_suggestions_query(uid))
            return [val[0] for val in result.values()]
        with self.driver.session() as session:
            return session.write_transaction(_get_follow_suggestions, uid)
            
    
    def get_following_list(self, uid: str):
        def _get_following_list(tx, uid: str):
            result = tx.run(CypherQueryGenerator.get_following_list_query(uid))
            return [val[0] for val in result.values()]
        with self.driver.session() as session:
            return session.write_transaction(_get_following_list, uid)

    
    def get_followers_list(self, uid: str):
        def _get_followers_list(tx, uid: str):
            result = tx.run(CypherQueryGenerator.get_followers_list_query(uid))
            return [val[0] for val in result.values()]
        with self.driver.session() as session:
            return session.write_transaction(_get_followers_list, uid)
            
    
    def close(self):
        self.driver.close()




class CypherQueryGenerator:
    @staticmethod
    def get_create_node_query(user: UserNode) -> str:
        return f"CREATE (n:User {{ uid:'{user.uid}', created_at:'{user.created_at}' }} )"
    @staticmethod
    def get_delete_node_query(user: UserNode) -> str:
        return f"MATCH (n:User {{ uid:'{user.uid}' }} ) DETACH DELETE n"
    @staticmethod
    def get_following_count_query(uid:str) -> str:
        return f"""MATCH (u: User{{uid: '{uid}' }}) RETURN size((u)-->()) AS degreeOut"""
    @staticmethod
    def get_followers_count_query(uid: str) -> str:
        return f"""MATCH (u: User{{uid: '{uid}' }}) RETURN size((u)<--()) AS degreeIn"""
    @staticmethod
    def get_create_relationship_query(relationship: UserRelationship) -> str:
        return f"""MATCH (a:User), (b:User)
                    WHERE a.uid = '{relationship.uid}' AND b.uid = '{relationship.uid2}'
                    CREATE (a)-[r:FOLLOWS {{created_at: '{relationship.created_at}' }}]->(b)"""
    
    @staticmethod
    def get_delete_relationship_query(relationship: UserRelationship) -> str:
        return f"""MATCH (a:User)-[r:FOLLOWS]->(b:User)
                    WHERE a.uid = '{relationship.uid}' AND b.uid = '{relationship.uid2}'
                    DELETE r"""

    
    @staticmethod
    def get_follow_suggestions_query(uid: str) -> str:
        return f"""MATCH (a:User{{uid:'{uid}'}})-[:FOLLOWS*2..3]->(b:User) RETURN distinct b.uid"""

    @staticmethod
    def get_following_list_query(uid: str) -> str:
        return f"""MATCH (a:User{{uid:'{uid}'}})-[:FOLLOWS]->(b:User) RETURN b.uid"""
    
    @staticmethod
    def get_followers_list_query(uid: str) -> str:
        return f"""MATCH (a:User{{uid:'{uid}'}})<-[:FOLLOWS]-(b:User) RETURN b.uid"""