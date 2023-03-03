
class Transcript(object):
    __type = 'Transcript'
 
    def __init__(self, args: dict = None) -> None:
        self._stable_id = args.get("stable_id")
        self._transcript_id = args.get("transcript_id")
        if args.get("version") is None:
            self._version = 1
        else:
            self._version = args.get("version")
        self._external_name = args.get("external_name")
        self._external_db = args.get("external_db")
        self._external_status = args.get("external_status")
        self._display_xref_id = args.get("display_xref_id")
        self._created_date = args.get("created_date")
        self._modified_date = args.get("modified_date")
        self._description = args.get("description")
        if args.get("is_current") is None:
            self._is_current = 1
        else:
            self._is_current = args.get("is_current")
        self._source = args.get("source")
        self._seq_region_name = args.get("seq_region_name")
        self._start = args.get("start")
        self._end = args.get("end")
        self._strand = args.get("strand")

    @property
    def stable_id(self) -> str:
        return self._stable_id

    @stable_id.setter
    def stable_id(self, value: str) -> None:
        self._stable_id = value

    @property
    def transcript_id(self) -> int:
        return self._transcript_id

    @transcript_id.setter
    def transcript_id(self, value: int) -> None:
        self._transcript_id = value

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, value: int) -> None:
        self._version = value

    @property
    def external_name(self) -> str:
        return self._external_name
        # TO DO: If not set, get from display xref

    @external_name.setter
    def external_name(self, value: str) -> None:
        self._external_name = value

    @property
    def external_db(self) -> str:
        return self._external_db
        # TO DO: If not set, get from display xref

    @external_db.setter
    def external_db(self, value: str) -> None:
        self._external_db = value

    @property
    def external_status(self) -> str:
        return self._external_status
        # TO DO: If not set, get from display xref

    @external_status.setter
    def external_status(self, value: str) -> None:
        self._external_status = value

    @property
    def display_xref_id(self) -> int:
        return self._display_xref_id

    @display_xref_id.setter
    def display_xref_id(self, value: int) -> None:
        self._display_xref_id = value

    @property
    def created_date(self) -> str:
        return self._created_date

    @created_date.setter
    def created_date(self, value: str) -> None:
        self._created_date = value

    @property
    def modified_date(self) -> str:
        return self._modified_date

    @modified_date.setter
    def modified_date(self, value: str) -> None:
        self._modified_date = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def is_current(self) -> bool:
        return self._is_current

    @is_current.setter
    def is_current(self, value: bool) -> None:
        self._is_current = value

    @property
    def source(self) -> str:
        if self._source is None:
            return "ensembl"
        return self._source

    @source.setter
    def source(self, value: str) -> None:
        self._source = value

    @property
    def seq_region_name(self) -> str:
        return self._seq_region_name

    @seq_region_name.setter
    def seq_region_name(self, value: str) -> None:
        self._seq_region_name = value

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, value: int) -> None:
        self._start = value

    @property
    def end(self) -> int:
        return self._end

    @end.setter
    def end(self, value: int) -> None:
        self._end = value

    @property
    def strand(self) -> int:
        return self._strand

    @strand.setter
    def strand(self, value: int) -> None:
        self._strand = value

    def display_id(self):
        if self._stable_id is not None:
            return self._stable_id
        else:
            return self._transcript_id

    def summary_as_hash(self) -> dict:
        summary = {}

        summary["seq_region_name"] = self._seq_region_name or "?"
        summary["source"] = self._source
        summary["start"] = self._start
        summary["end"] = self._end
        summary["strand"] = self._strand
        summary["ID"] = self.display_id()
        summary["transcript_id"] = self.display_id()
        summary["description"] = self._description
        summary["version"] = self._version
        summary["Name"] = self._external_name

        return summary
