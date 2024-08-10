import os
import tomllib
from typing import Dict, Any, List

TomlExpr = Dict[str, Any]

def toml_from_file(path: str) -> TomlExpr:
    with open(path, "rb") as file:
        data: TomlExpr = tomllib.load(file)
    return data

def extract_websites(data: TomlExpr) -> Dict[str, str]:
    return {id : info['website']
        for id, info in data.items()}

def gen_website_list(data_path: str, levels: List[str]) -> Dict[str, str]:
    toml_files = [os.path.join(data_path, f"{level}.toml")
        for level in levels]

    unioned_websites = {}
    for toml_file in toml_files:
        data = toml_from_file(toml_file)
        websites = extract_websites(data)
        for (id, website) in websites.items():
            assert id not in unioned_websites, f"Duplicate name ID: {id}"
            unioned_websites[id] = website
    return unioned_websites
