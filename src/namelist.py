from io import StringIO
from .utils import toml_from_file, TomlExpr
import tomllib
from mako.runtime import Context
from mako.template import Template
from typing import Any

def sort_by_last_name(data: TomlExpr) -> TomlExpr:
    return dict(sorted(data.items(), key=lambda item: item[1]['name'].split()[-1]))

def gen_name_ul(data: TomlExpr, template_path: str):
    template: Template = Template(filename=template_path)
    name_ul = template.render(data=data)
    return name_ul

def gen_name_lists(data_path: str, template_path: str, levels: list[str]) -> dict[str, bytes | str]:
    def gen_name_list(level: str):
        data = sort_by_last_name(toml_from_file(f"{data_path}/{level}.toml"))
        return gen_name_ul(data, template_path)
    return {level: gen_name_list(level) for level in levels}
