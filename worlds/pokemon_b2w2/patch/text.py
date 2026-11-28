import string


debug_flags = set()


class Entry:
    line: str = "[Terminate]"
    key: int = 1
    flags: int = 0

    def __init__(self, line="[Terminate]", key=1, flags=0):
        super().__init__()
        self.line = line
        self.key = key
        self.flags = flags


def decode(data: bytes, print_decode: bool = False) -> list[list[Entry]]:

    pointer = [0]

    def read(a: int) -> int:
        pointer[0] += a
        return int.from_bytes(data[pointer[0]-a:pointer[0]], "little")

    def seek(a: int) -> None:
        pointer[0] = a

    numblocks = read(2)
    numentries = read(2)
    blocksizesum = read(4)
    zero = read(4)

    blockoffsets = [0 for _ in range(numblocks)]
    tableoffsets = [[0 for _ in range(numentries)] for _ in range(numblocks)]
    charcounts = [[0 for _ in range(numentries)] for _ in range(numblocks)]
    texts = [[Entry() for _ in range(numentries)] for _ in range(numblocks)]

    for i in range(numblocks):
        blockoffsets[i] = read(4)
    for i in range(numblocks):
        seek(blockoffsets[i])
        blocksize = read(4)
        for j in range(numentries):
            tableoffsets[i][j] = read(4)
            charcounts[i][j] = read(2)
            texts[i][j].flags = read(2)
        for j in range(numentries):
            encchars = []
            decchars = []
            st = texts[i][j]
            st.line = ""
            seek(blockoffsets[i] + tableoffsets[i][j])
            for k in range(charcounts[i][j]):
                encchars.append(read(2))
            st.key = encchars[-1] ^ 0xFFFF
            while len(encchars):
                decchars.insert(0, encchars.pop() ^ st.key)
                st.key = ((st.key >> 3) | (st.key << 13)) & 0xFFFF
            k = 0
            while k < len(decchars):
                char = decchars[k]
                if char == 0xFFFF:
                    if k != len(decchars) - 1:
                        st.line += "[Terminate]"
                elif char == 0xFFFE:
                    st.line += "[NextLine]"  # \n in ctrmap
                elif char == 0xF000:
                    k += 1
                    command = decchars[k]
                    k += 1
                    total = decchars[k]
                    if command == 0xBE01 and total == 0:
                        st.line += f"[End]"  # \c in ctrmap
                    elif command == 0xBE00 and total == 0:
                        st.line += f"[Scroll]"  # \r in ctrmap
                    else:
                        st.line += f"[c_{command:x}_#{total}"
                        for _ in range(total):
                            k += 1
                            st.line += f"_{decchars[k]}"
                        st.line += "]"
                elif char in (0x100, 0xFF00):
                    k += 1
                    total = decchars[k]
                    st.line += f"[d_{char:x}_#{total}"
                    for _ in range(total):
                        k += 1
                        st.line += f"_{decchars[k]}"
                    st.line += "]"
                elif 20 < char <= 0xD7FF or 0xE000 <= char < 0xF000:
                    st.line += char.to_bytes(2, "little").decode("utf-16")
                else:
                    st.line += f"[{hex(char)}]"
                k += 1

    return texts


def encode(texts: list[list[Entry]]) -> bytes:

    # Format:
    # Numblocks: 2, numentries: 2, blocksizesum: 4, zero: 4, blockoffsets: 4*numblocks
    # in every block:
    #   Blocksize: 4, (offset: 4, charcount: 2, flags: 2)*numentries, (chars: x)*numentries

    data = bytearray()
    blocksizesum = 0

    data += len(texts).to_bytes(2, "little")
    numentries = max(len(entries) for entries in texts)
    for entries in texts:
        if len(entries) != numentries:
            raise Exception(f"Unequal count of entries in different text blocks: max {numentries}, found {len(entries)}")
    data += numentries.to_bytes(2, "little")
    data += b'\0\0\0\0\0\0\0\0'  # blocksizesum

    for i in range(len(texts)):
        data += b'\0\0\0\0'  # blockoffset
    for i in range(len(texts)):
        blockoffset = len(data)
        data[4*i+12:4*i+16] = blockoffset.to_bytes(4, "little")
        data += b'\0\0\0\0'  # blocksize
        for j in range(len(texts[i])):
            entry = texts[i][j]
            data += b'\0\0\0\0'  # tableoffset
            data += b'\0\0'  # charcount
            data += entry.flags.to_bytes(2, "little")
        for j in range(len(texts[i])):
            tableoffset = len(data)-blockoffset
            data[8*j+blockoffset+4:8*j+blockoffset+8] = tableoffset.to_bytes(4, "little")
            entry = texts[i][j]
            decchars: list[int] = []  # Ordered from first to last char
            k = 0
            while k < len(entry.line):
                char = entry.line[k]
                if char != "[":
                    if char == "]":
                        raise Exception(f"Extra closing bracket: "+entry.line[:k+1])
                    unicode = ord(char)
                    if unicode > 0xffff:
                        raise Exception(f"Unicode character cannot be written to text file: {char} ({hex(unicode)})")
                    decchars.append(unicode)
                    k += 1
                else:
                    if k + 10 < len(entry.line) and entry.line[k:k+11] == "[Terminate]":
                        decchars.append(0xffff)
                        k += 11
                    elif k + 9 < len(entry.line) and entry.line[k:k+10] == "[NextLine]":
                        decchars.append(0xfffe)
                        k += 10
                    elif k + 4 < len(entry.line) and entry.line[k:k+5] == "[End]":
                        decchars.extend([0xf000, 0xbe01, 0])
                        k += 5
                    elif k + 7 < len(entry.line) and entry.line[k:k+8] == "[Scroll]":
                        decchars.extend([0xf000, 0xbe00, 0])
                        k += 8
                    elif k + 4 < len(entry.line) and entry.line[k:k+3] == "[0x":
                        end = entry.line.find("]", k)
                        if end == -1:
                            raise Exception("Unclosed raw value: "+entry.line[k:])
                        raw = int(entry.line[k+1:end], 16)
                        if raw > 0xffff:
                            raise Exception("Unsupported raw number: "+entry.line[k+1:end])
                        decchars.append(raw)
                        k = end + 1
                    elif k + 2 < len(entry.line) and entry.line[k:k+3] == "[c_":
                        end = entry.line.find("]", k)
                        if end == -1:
                            raise Exception("Unclosed command: "+entry.line[k:])
                        parts = entry.line[k+1:end].split("_")
                        if len(parts) < 3:
                            raise Exception("Incomplete command: "+entry.line[k+1:end])
                        if parts[2][0] != "#":
                            raise Exception("Bad command formatting: "+entry.line[k+1:end])
                        if int(parts[2][1:]) != len(parts) - 3:
                            raise Exception("Incorrect value count for command: "+entry.line[k+1:end])
                        decchars.extend([0xf000, int(parts[1], 16), int(parts[2][1:])])
                        decchars.extend(int(part) for part in parts[3:])
                        k = end + 1
                    elif k + 2 < len(entry.line) and entry.line[k:k+3] == "[d_":
                        end = entry.line.find("]", k)
                        if end == -1:
                            raise Exception("Unclosed command: "+entry.line[k:])
                        parts = entry.line[k+1:end].split("_")
                        if len(parts) < 3:
                            raise Exception("Incomplete command: "+entry.line[k+1:end])
                        if parts[2][0] != "#":
                            raise Exception("Bad command formatting: "+entry.line[k+1:end])
                        if int(parts[2][1:]) != len(parts) - 3:
                            raise Exception("Incorrect value count for command: "+entry.line[k+1:end])
                        decchars.extend([int(parts[1], 16), int(parts[2][1:])])
                        decchars.extend(int(part) for part in parts[3:])
                        k = end + 1
                    else:
                        end = entry.line.find("]", k)
                        raise Exception("Bad special characters: "+(entry.line[k+1:end] if end != -1 else entry.line[k+1]))
            if not decchars or decchars[-1] != 0xffff:
                decchars.append(0xffff)
            encchars: list[int] = []
            if getattr(entry, "key", None) is not None:
                key = entry.key
            else:
                k_init = ((j + 3) * 0x2983) & 0xFFFF
                key = ((k_init >> 3) | (k_init << 13)) & 0xFFFF
            for decoded in decchars:
                key = ((key << 3) & 0xffff) | (key >> 13)
                encchars.append(decoded ^ key)
            for encoded in encchars:
                data += encoded.to_bytes(2, "little")
            data[8*j+blockoffset+8:8*j+blockoffset+10] = len(encchars).to_bytes(2, "little")  # charcount
        blocksize = len(data) - blockoffset
        blocksizesum += blocksize
        data[blockoffset:blockoffset+4] = blocksize.to_bytes(4, "little")  # blocksize
    data[4:8] = blocksizesum.to_bytes(4, "little")

    return data


def is_bad_text(line: str) -> str:
    k = 0
    while k < len(line):
        char = line[k]
        if char == "]":
            return "Extra closing bracket"
        if char == "[":
            if k + 10 < len(line) and line[k:k+11] == "[Terminate]":
                k += 11
                if k == len(line):
                    return ""
                return "[Terminate] before end of line"
            elif k + 9 < len(line) and line[k:k + 10] == "[NextLine]":
                k += 10
            elif k + 4 < len(line) and line[k:k+5] == "[End]":
                k += 5
            elif k + 7 < len(line) and line[k:k+8] == "[Scroll]":
                k += 8
            elif k + 4 < len(line) and line[k:k+3] == "[0x":
                end = line.find("]", k)
                if end == -1:
                    return "Missing closing bracket"
                if not line[k+3:end].isnumeric():
                    return "Non-numeric raw value"
                if int(line[k+1:end]) > 0xffff:
                    return "Raw value too big"
                k = end + 1
            elif k + 2 < len(line) and line[k:k+3] == "[c_":
                end = line.find("]", k)
                if end == -1:
                    return "Missing closing bracket"
                parts = line[k+1:end].split("_")
                if len(parts) < 3:
                    return "Incomplete command"
                if parts[2][0] != "#":
                    return "Missing # at command param count"
                if not parts[2][1:].isnumeric():
                    return "Non-numeric command param count"
                if int(parts[2][1:]) != len(parts) - 3:
                    return "Incorrect command param count"
                if not all(c in string.hexdigits for c in parts[1]):
                    return "Command is not a hexadecimal number"
                for part in parts[3:]:
                    if not part.isnumeric():
                        return "Non-numeric command param"
                k = end + 1
        else:
            k += 1
    return "Line ended without [Terminate]"

def encode_single_entry(line: str, key: int = 0xadd5) -> tuple[int, bytes]:
    data = encode([[Entry(line=line, key=key)]])
    charcount = int.from_bytes(data[24:26], "little")
    chars_data = bytes(data[28:])
    return charcount, chars_data


def insert_line(text_file: list[list[Entry]], block_num: int, line_num: int, text: str, key: int | None = None) -> None:
    # Inserts or overwrites a line at the given block and line index
    copy_flags = 0 if len(text_file[0]) == 0 else text_file[0][0].flags
    while block_num >= len(text_file):
        text_file.append([Entry(key=None, flags=copy_flags) for _ in range(len(text_file[0]))])
    while line_num >= len(text_file[0]):
        for block in text_file:
            block.append(Entry(key=None, flags=copy_flags))
    text_file[block_num][line_num].line = text
    text_file[block_num][line_num].key = key


def _sanitize_text(text: str) -> str:
    # Escapes brackets and non-BMP characters so AP strings cannot break Gen 5 text encoding
    text = text.replace("[", "(").replace("]", ")")
    return "".join(ch if ord(ch) <= 0xFFFF else "?" for ch in text)


def apply_check_text(rom: object, slot_data: dict) -> None:
    # Patches a/0/0/3 text file 437 with custom textboxes
    try:
        from ..nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import NARC

    narc_story = NARC(rom.getFileByName("a/0/0/3"))
    text_437 = decode(narc_story.files[437])
    ref_keys = [e.key for e in decode(narc_story.files[609])[0]]

    loc_check_info = slot_data.get("loc_check_info", {})
    all_flags = sorted(int(k) for k in loc_check_info.keys())
    recipient_label = _sanitize_text(str(slot_data.get("recipient_label", "another world")))

    k20 = ref_keys[20] if 20 < len(ref_keys) else None
    insert_line(text_437, 0, 20, f"[c_100_#1_0] sent an item[NextLine]to {recipient_label}!", key=k20)

    for i, f_id in enumerate(all_flags):
        text_id = 21 + i
        item_name, player_name, classification, is_local = loc_check_info[str(f_id)]
        item_name = _sanitize_text(str(item_name))
        player_name = _sanitize_text(str(player_name))
        if classification & 1:
            color_code = 6  # Progression
        elif classification & 4:
            color_code = 1  # Trap
        elif classification & 2:
            color_code = 3  # Useful
        else:
            color_code = 0  # Filler

        color_tag = f"[c_ff00_#1_{color_code}]" if color_code != 0 else ""
        reset_tag = "[c_ff00_#1_0]" if color_code != 0 else ""
        k_entry = ref_keys[text_id] if text_id < len(ref_keys) else None
        if is_local:
            msg = f"[c_100_#1_0] found {color_tag}{item_name}{reset_tag}!"
        else:
            msg = f"[c_100_#1_0] sent {color_tag}{item_name}{reset_tag}[NextLine]to {player_name}!"

        insert_line(
            text_437,
            0,
            text_id,
            msg,
            key=k_entry,
        )

    narc_story.files[437] = encode(text_437)
    rom.setFileByName("a/0/0/3", narc_story.save())
