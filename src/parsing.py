from src.connection import Connection
from src.graph import Graph
from src.zone import Zone, ZoneType


class ParseError(Exception):
    """Raised when a map file does not follow the expected format."""

    def __init__(self, line_number: int, message: str) -> None:
        self.line_number = line_number
        self.message = message
        super().__init__(f"line {line_number}: {message}")


class Parser:
    """Reads a network description file and builds a Graph.

    Comments "#" and empty lines are ignored.
    """

    def __init__(self) -> None:
        self._graph = Graph()
        self._nb_drones: int | None = None

    def parse(self, path: str) -> tuple[Graph, int]:
        """Parse a map file into a Graph, raising ParseError if malformed."""
        self._graph = Graph()
        self._nb_drones = None
        with open(path, encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                self._parse_line(line_number, raw_line)
        if self._nb_drones is None:
            raise ParseError(0, "missing 'nb_drones:' declaration")
        if not self._has_start_and_end():
            raise ParseError(0, "missing start_hub or end_hub")
        return self._graph, self._nb_drones

    def _has_start_and_end(self) -> bool:
        try:
            self._graph.start
            self._graph.end
        except ValueError:
            return False
        return True

    def _parse_line(self, line_number: int, raw_line: str) -> None:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            return
        if self._nb_drones is None:
            self._parse_nb_drones(line_number, line)
        elif line.startswith("start_hub:"):
            self._parse_zone(line_number, line, "start_hub:", is_start=True)
        elif line.startswith("end_hub:"):
            self._parse_zone(line_number, line, "end_hub:", is_end=True)
        elif line.startswith("hub:"):
            self._parse_zone(line_number, line, "hub:")
        elif line.startswith("connection:"):
            self._parse_connection(line_number, line)
        else:
            raise ParseError(line_number, f"unrecognized directive: {line!r}")

    def _parse_nb_drones(self, line_number: int, line: str) -> None:
        if not line.startswith("nb_drones:"):
            raise ParseError(
                line_number, "expected 'nb_drones:' as the first directive"
            )
        value = line[len("nb_drones:"):].strip()
        self._nb_drones = self._parse_positive_int(
            line_number, "nb_drones", value
        )

    def _parse_zone(
        self,
        line_number: int,
        line: str,
        prefix: str,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        body = line[len(prefix):].strip()
        fields, metadata = self._split_metadata(line_number, body)
        tokens = fields.split()
        if len(tokens) != 3:
            raise ParseError(
                line_number, f"expected '<name> <x> <y>', got {fields!r}"
            )
        name, x_str, y_str = tokens
        self._validate_name(line_number, name)
        zone_type = ZoneType.NORMAL
        if "zone" in metadata:
            zone_type = self._parse_zone_type(line_number, metadata["zone"])
        max_drones = 1
        if "max_drones" in metadata and not (is_start or is_end):
            max_drones = self._parse_positive_int(
                line_number, "max_drones", metadata["max_drones"]
            )
        zone = Zone(
            name=name,
            x=self._parse_int(line_number, "x", x_str),
            y=self._parse_int(line_number, "y", y_str),
            zone_type=zone_type,
            color=metadata.get("color"),
            max_drones=max_drones,
            is_start=is_start,
            is_end=is_end,
        )
        try:
            self._graph.add_zone(zone)
        except ValueError as exc:
            raise ParseError(line_number, str(exc)) from exc

    def _parse_connection(self, line_number: int, line: str) -> None:
        body = line[len("connection:"):].strip()
        fields, metadata = self._split_metadata(line_number, body)
        if "-" not in fields:
            raise ParseError(
                line_number, f"expected '<name1>-<name2>', got {fields!r}"
            )
        name_a, _, name_b = fields.partition("-")
        zone_a = self._resolve_zone(line_number, name_a)
        zone_b = self._resolve_zone(line_number, name_b)
        capacity = 1
        if "max_link_capacity" in metadata:
            capacity = self._parse_positive_int(
                line_number,
                "max_link_capacity",
                metadata["max_link_capacity"],
            )
        connection = Connection(zone_a, zone_b, max_link_capacity=capacity)
        try:
            self._graph.add_connection(connection)
        except ValueError as exc:
            raise ParseError(line_number, str(exc)) from exc

    def _resolve_zone(self, line_number: int, name: str) -> Zone:
        try:
            return self._graph.get_zone(name.strip())
        except KeyError:
            raise ParseError(
                line_number, f"connection references unknown zone: {name!r}"
            ) from None

    @staticmethod
    def _split_metadata(
        line_number: int, text: str
    ) -> tuple[str, dict[str, str]]:
        if "[" not in text:
            return text.strip(), {}
        if not text.endswith("]"):
            raise ParseError(line_number, "malformed metadata block")
        before, _, block = text.partition("[")
        metadata: dict[str, str] = {}
        for token in block[:-1].split():
            if "=" not in token:
                raise ParseError(
                    line_number, f"malformed metadata tag: {token!r}"
                )
            key, _, value = token.partition("=")
            metadata[key] = value
        return before.strip(), metadata

    @staticmethod
    def _validate_name(line_number: int, name: str) -> None:
        if "-" in name or " " in name:
            raise ParseError(
                line_number,
                f"zone name cannot contain '-' or spaces: {name!r}",
            )

    @staticmethod
    def _parse_zone_type(line_number: int, value: str) -> ZoneType:
        try:
            return ZoneType(value)
        except ValueError:
            raise ParseError(
                line_number, f"invalid zone type: {value!r}"
            ) from None

    @staticmethod
    def _parse_int(line_number: int, field: str, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ParseError(
                line_number, f"invalid integer for {field}: {value!r}"
            ) from None

    @staticmethod
    def _parse_positive_int(
        line_number: int, field: str, value: str
    ) -> int:
        parsed = Parser._parse_int(line_number, field, value)
        if parsed <= 0:
            raise ParseError(
                line_number,
                f"{field} must be a positive integer, got {parsed}",
            )
        return parsed
