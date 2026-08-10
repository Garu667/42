import sys
from src.parsing import Parser

def test() -> None:
    if len(sys.argv) != 2:
        print("file")
        sys.exit(1)
    path = sys.argv[1]
    graph, nb_drones = Parser().parse(path)
    print(f"nb_drones = {nb_drones}")
    print(f"zones     = {len(graph)}")
    print(f"start     = {graph.start!r}")
    print(f"end       = {graph.end!r}")
    print("\nzones:")
    for zone in graph.zones:
        print(
            f"  {zone.name:<15} ({zone.x:>3},{zone.y:>3})  "
            f"type={zone.zone_type.value:<10} "
            f"capacity={zone.capacity}"
        )
    print("\nconnections:")
    seen = set()
    for zone in graph.zones:
        for neighbor, connection in graph.neighbors(zone):
            if connection.name in seen:
                continue
            seen.add(connection.name)
            print(
                f"  {connection.name:<25} cap={connection.max_link_capacity}"
            )


def main() -> None:
    test()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
