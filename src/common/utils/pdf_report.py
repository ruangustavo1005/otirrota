import os
from typing import Any, Dict, Optional, Tuple
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa


class PDFReport:
    def __init__(self, template_path: str, save_path: Optional[str] = None) -> None:
        self.__env = Environment(
            loader=FileSystemLoader(os.path.dirname(template_path))
        )
        self.__template = self.__env.get_template(os.path.basename(template_path))
        self.__save_path = save_path or os.path.join(
            os.path.expanduser("~"), "Downloads"
        )

    def render_and_save(
        self, data: Dict[str, Any], output_filename: str
    ) -> Tuple[bool, str]:
        html = self.__template.render(data)
        output_filepath = os.path.join(self.__save_path, output_filename)
        with open(output_filepath, "wb") as result_file:
            pisa_status = pisa.CreatePDF(html, dest=result_file)
        return not pisa_status.err, output_filepath
