from __future__ import annotations

from pathlib import Path
from typing import Iterable

try:
    from .apnds.code import CodeStartParams
    from .apnds.lz import compress_code, decompress_code
    from .apnds.narc import Narc
    from .apnds.rom import HeaderField, Overlay, Rom
except (ImportError, ValueError):
    from apnds.code import CodeStartParams
    from apnds.lz import compress_code, decompress_code
    from apnds.narc import Narc
    from apnds.rom import HeaderField, Overlay, Rom


def _norm_path(name: str) -> str:
    return name if name.startswith("/") else "/" + name


class NARC:
    def __init__(self, data: bytes | bytearray | None = None):
        if data is None:
            self._narc = Narc()
        else:
            self._narc = Narc.from_bytes(bytes(data))
        self.files: list[bytes] = list(self._narc.files)

    def save(self) -> bytes:
        self._narc.files = list(self.files)
        return self._narc.to_bytes()


class OverlayWrapper:
    def __init__(self, ov: Overlay, index: int):
        self._ov = ov
        self.id: int = ov.id
        self.ramAddress: int = ov.ram_address
        self.ramSize: int = ov.ram_size
        self.bssSize: int = ov.bss_size
        self.sinitInit: int = ov.sinit_init
        self.sinitInitEnd: int = ov.sinit_init_end
        self.fileID: int = -(index + 1)
        self.compressed: bool = ov.is_compressed()
        if self.compressed:
            dec, _ = decompress_code(ov.data, len(ov.data))
            self.data: bytes = dec
        else:
            self.data = ov.data

    def save(self, compress: bool = False) -> bytes:
        raw = bytes(self.data)
        self.ramSize = len(raw)
        self._ov.ram_size = len(raw)
        if compress:
            comp = compress_code(raw)
            if comp is not None:
                self._ov.data = comp
                self._ov.flags |= 1
                self._ov.compressed_size = len(comp)
                self.compressed = True
                return comp
        self._ov.data = raw
        self._ov.flags &= ~1
        self._ov.compressed_size = 0
        self.compressed = False
        return raw


class _FilesProxy:
    # Supports both path keys and synthetic overlay fileIDs
    def __init__(self, rom: Rom):
        self._rom = rom
        self._ov_dummy: dict[int, bytes] = {}

    def __getitem__(self, key: str | int) -> bytes:
        if isinstance(key, int):
            if key < 0:
                idx = -key - 1
                return self._rom.arm9_overlays[idx].data
            return self._ov_dummy[key]
        return self._rom.files[_norm_path(key)]

    def __setitem__(self, key: str | int, value: bytes | bytearray) -> None:
        if isinstance(key, int):
            if key < 0:
                return
            self._ov_dummy[key] = bytes(value)
            return
        self._rom.files[_norm_path(key)] = bytes(value)


class _FilenamesProxy:
    def __getitem__(self, name: str) -> str:
        return _norm_path(name)

    def __contains__(self, name: str) -> bool:
        return True


class NintendoDSRom:
    def __init__(self, data: bytes | bytearray | None = None):
        if data is None:
            raise ValueError("NintendoDSRom requires ROM bytes; use fromFile or pass bytes")
        self._rom: Rom = Rom.from_bytes(bytes(data), decrypt_modcrypt=False)
        self.files = _FilesProxy(self._rom)
        self.filenames = _FilenamesProxy()
        self._arm9_overlay_table: bytes = b""

    @classmethod
    def fromFile(cls, filePath: str | Path) -> "NintendoDSRom":
        return cls(Path(filePath).read_bytes())

    @property
    def name(self) -> bytes:
        return bytes(self._rom.header[HeaderField.TITLE])

    @property
    def idCode(self) -> bytes:
        return bytes(self._rom.header[HeaderField.SERIAL])

    @property
    def arm9(self) -> bytes:
        return self._rom.arm9

    @arm9.setter
    def arm9(self, value: bytes | bytearray) -> None:
        self._rom.arm9 = bytes(value)

    @property
    def arm9RamAddress(self) -> int:
        return self._rom.header.get_le(HeaderField.ARM9_LOADADDR)

    @property
    def arm9EntryAddress(self) -> int:
        return self._rom.header.get_le(HeaderField.ARM9_ENTRYPOINT)

    @property
    def arm9OverlayTable(self) -> bytes:
        return self._arm9_overlay_table

    @arm9OverlayTable.setter
    def arm9OverlayTable(self, value: bytes | bytearray) -> None:
        self._arm9_overlay_table = bytes(value)

    @property
    def pad088(self) -> bytes:
        return bytes(self._rom.header.data[0x088:0x0C0])

    @pad088.setter
    def pad088(self, value: bytes | bytearray) -> None:
        raw = bytes(value)
        if len(raw) != 0x38:
            raw = (raw + bytes(0x38))[:0x38]
        self._rom.header.data[0x088:0x0C0] = raw

    def getFileByName(self, filename: str) -> bytes | None:
        return self._rom.files.get(_norm_path(filename))

    def setFileByName(self, filename: str, data: bytes | bytearray) -> None:
        self._rom.files[_norm_path(filename)] = bytes(data)

    def loadArm9Overlays(self, idsToLoad: Iterable[int] | None = None) -> dict[int, OverlayWrapper]:
        wanted = set(idsToLoad) if idsToLoad is not None else None
        out: dict[int, OverlayWrapper] = {}
        for idx, ov in enumerate(self._rom.arm9_overlays):
            if wanted is None or ov.id in wanted:
                out[ov.id] = OverlayWrapper(ov, idx)
        return out

    def save(self, updateDeviceCapacity: bool = False) -> bytes:
        return self._rom.to_bytes()

    def saveToFile(self, filePath: str | Path, updateDeviceCapacity: bool = False) -> None:
        Path(filePath).write_bytes(self.save(updateDeviceCapacity=updateDeviceCapacity))


def saveOverlayTable(table: dict[int, OverlayWrapper]) -> bytes:
    return b""


class _CodeCompression:
    @staticmethod
    def decompress(data: bytes | bytearray, load_address: int = 0x02004000) -> bytes:
        raw = bytes(data)
        csp = CodeStartParams.from_code(raw, load_address)
        if csp is not None and csp.compressed_end:
            top = csp.compressed_end - load_address
            if 0 < top <= len(raw):
                dec, tail = decompress_code(raw, top)
                return dec + tail
        dec, tail = decompress_code(raw, len(raw))
        return dec + tail

    @staticmethod
    def compress(data: bytes | bytearray, isArm9: bool = False, load_address: int = 0x02004000) -> bytes:
        raw = bytes(data)
        if isArm9:
            csp = CodeStartParams.from_code(raw, load_address)
            if csp is not None and len(raw) > 0x4000:
                comp_tail = compress_code(raw[0x4000:])
                if comp_tail is not None:
                    buf = raw[:0x4000] + comp_tail
                    csp.compressed_end = load_address + len(buf)
                    return csp.write_start_info(buf, load_address)
            if csp is not None:
                csp.compressed_end = 0
                return csp.write_start_info(raw, load_address)
            return raw
        comp = compress_code(raw)
        return comp if comp is not None else raw


codeCompression = _CodeCompression()
