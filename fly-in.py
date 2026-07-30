from src.zone import Zone, ZoneType
from src.connection import Connection
from src.graph import Graph

def test_graph() -> Graph:
    graph = Graph()
    start = Zone("hub", 0, 0, is_start=True)
    end = Zone("goal", 10, 10, is_end=True)
    roof1 = Zone("roof1", 3, 4, zone_type=ZoneType.RESTRICTED)
    roof2 = Zone("roof2", 6, 2, zone_type=ZoneType.NORMAL)
    corridor = Zone("corridor", 4, 3, zone_type=ZoneType.PRIORITY, max_drones=4)
    tunnel = Zone("tunnel", 7, 4, zone_type=ZoneType.NORMAL)
    obstacle = Zone("obstacle", 5, 5, zone_type=ZoneType.BLOCKED)

    for zone in (start, end, roof1, roof2, corridor, tunnel, obstacle):
        graph.add_zone(zone)
    graph.add_connection(Connection(start, roof1))
    graph.add_connection(Connection(roof1, roof2))
    graph.add_connection(Connection(roof2, end))
    graph.add_connection(Connection(start, corridor))
    graph.add_connection(Connection(corridor, tunnel, max_link_capacity=4))
    graph.add_connection(Connection(tunnel, end))

    return graph

def main() -> None:
    graph = test_graph()
    corridor = graph.get_zone("corridor")
    print(f"{corridor} --- {corridor.capacity}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
