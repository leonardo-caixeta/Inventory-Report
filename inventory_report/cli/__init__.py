import os
from pathlib import Path
from typing import List

import rich
import typer
from rich import panel
from typing_extensions import Annotated

from inventory_report.cli.input_handler import process_report_request
from inventory_report.reports import REPORTS

typer_app = typer.Typer(no_args_is_help=True)

console = rich.get_console()


def validate_dir(dir_path: str) -> str:
    """Validate if the path is a directory"""
    if not Path(dir_path).is_dir():
        raise typer.BadParameter("Directory path is invalid.")
    return dir_path


def _get_inner_files(dir_path: str) -> List[str]:
    """Get the files inside the directory"""
    return [
        os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)
    ]


@typer_app.command(no_args_is_help=True)
def main(
    dir_path: Annotated[
        str,
        typer.Option(
            ...,
            "-p",
            help="Path to the directory containing the files to be imported",
            callback=validate_dir,
        ),
    ],
    report_type: Annotated[
        str,
        typer.Option(
            ...,
            "-t",
            help="Type of report to be generated",
            autocompletion=lambda: REPORTS,
        ),
    ],
) -> None:
    """Shows rich pannel with the return of the report function"""

    file_paths = _get_inner_files(dir_path)

    report = process_report_request(file_paths, report_type)

    rich.print(
        panel.Panel(
            report,
            title="Inventory Report",
            expand=False,
            highlight=True,
            border_style="green",
        )
    )
