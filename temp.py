from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_person(tx, name):
    tx.run("CREATE (a:Person {name: $name})", name=name)

def create_friend_of(tx, name, friend):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
           name=name, friend=friend)

with driver.session() as session:
    session.execute_write(create_person, "Alice")
    session.execute_write(create_friend_of, "Alice", "Bob")
    session.execute_write(create_friend_of, "Alice", "Carl")

driver.close()

