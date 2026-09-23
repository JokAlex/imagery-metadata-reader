from pathlib import Path
import xml.etree.ElementTree as ET


class Sentinel2MetadataParser:
    def __init__(self, metadata_path: Path):
        self._metadata_path = metadata_path

    def parse(self) -> dict:
        tree = ET.parse(self._metadata_path)
        root = tree.getroot()
        result: dict = {}
        for child in root:
            self._flatten(child, "", result)
        return result

    def _flatten(self, element, prefix: str, result: dict) -> None:
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        current_prefix = f"{prefix}/{tag}" if prefix else tag

        if len(element) == 0:
            text = (element.text or "").strip()
            if not text:
                return
            if current_prefix in result:
                existing = result[current_prefix]
                if isinstance(existing, list):
                    existing.append(text)
                else:
                    result[current_prefix] = [existing, text]
            else:
                result[current_prefix] = text
        else:
            for child in element:
                self._flatten(child, current_prefix, result)
