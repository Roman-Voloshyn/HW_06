import os
import sys
import shutil
from pathlib import Path


TRANS = {
            1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G',
            1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 
            1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 
            1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 
            1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 
            1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 
            1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 
            1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 
            1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
        }


CATEGORIES = {  
                'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
                'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF'),
                'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
                'video': ('AVI', 'MP4', 'MOV', 'MKV'),
                'archives': ('ZIP', 'GZ', 'TAR')
            }


def normalize(name: str) -> str:  
    name = name.translate(TRANS)
    for ch in name:
        if not 'a' <= ch <= 'z' and not 'A' <= ch <= 'Z' and not '0' <= ch <= '9':
            name = name.replace(ch , "_")
    return name


def rename_archives(path: Path):
    for item in path.iterdir(): 
        if item.is_dir():
            rename_archives(item)
        else:
            file_extension = item.suffix[1:].upper() 
            file_name = normalize(item.stem) + '.' + file_extension.lower()
            shutil.move(item, path / file_name)

        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
        elif item.is_dir():
            shutil.move(item, path / normalize(item.stem))


def sort_folder(path: Path):
    for item in path.iterdir():
        if item.is_dir() and item.stem not in CATEGORIES: 
            sort_folder(item)
        else:
            file_extension = item.suffix[1:].upper() 
            file_name = normalize(item.stem) + '.' + file_extension.lower()
            if file_extension in sum(CATEGORIES.values(), ()):
                for category, extensions in CATEGORIES.items():
                    if file_extension in extensions:
                        if category == 'archives':
                            shutil.unpack_archive(item, PATH / category / normalize(item.stem))
                            shutil.move(item, path / file_name)
                        else:
                            os.renames(item, PATH / category / file_name)
                        break
            else:
                shutil.move(item, path / file_name)

    for item in PATH.iterdir():
        if item.stem == 'archives':
            rename_archives(item)
    for item in path.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
        elif item.is_dir():
            shutil.move(item, path / normalize(item.stem))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        PATH = Path(sys.argv[1])
        sort_folder(PATH)
        print("Folder sorted")
    else:
        print('Incorrect command')
        sys.exit()