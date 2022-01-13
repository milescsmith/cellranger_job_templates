"""Console script for cellranger_job_templates."""
from typing import List, Optional, Tuple

import re
from enum import Enum
from pathlib import Path, home

import numpy as np
import pandas as pd
import typer
from cellranger_job_templates.logging import crjt_logger as logger

app = typer.Typer()


class StatusMessage(str, Enum):
    END = "END"
    FAIL = "FAIL"
    START = "START"
    NONE = "NONE"
    BEGIN = "BEGIN"
    REQUEUE = "REQUEUE"
    ALL = "ALL"
    INVALID_DEPEND = "INVALID_DEPEND"
    STAGE_OUT = "STAGE_OUT"
    TIME_LIMIT = "TIME_LIMIT"
    TIME_LIMIT_90 = "TIME_LIMIT_90"
    TIME_LIMIT_80 = "TIME_LIMIT_80"
    TIME_LIMIT_50 = "TIME_LIMIT_50"
    ARRAY_TASKS = "ARRAY_TASKS"


class Chemistry(str, Enum):
    auto = "auto"
    threeprime = "threeprime"
    fiveprime = "fiveprime"
    SC3Pv1 = "SC3Pv1"
    SC3Pv2 = "SC3Pv2"
    SC3Pv3 = "SC3Pv3"
    SC5P_PE = "SC5P-PE"
    SC5P_R2 = "SC5P-R2"
    SC_FB = "SC-FB"


def extract_subdir_files(
    subdir: Path,
    libtype: str,
) -> Tuple[List[str], List[str], List[str]]:
    illumina_pattern = re.compile(r"\S+(?=_S\d+_R\d+_\d+\.fastq\.gz)")

    seq_files = list(subdir.glob("*.fastq.gz"))
    fq_files = [str(subdir.resolve())] * (len(seq_files) // 2)
    names = np.unique([illumina_pattern.match(_.name)[0] for _ in seq_files])
    if libtype == "adt" or libtype == "hto":
        lib_descript = ["Antibody Capture"] * (len(seq_files) // 2)
    elif libtype == "gex":
        lib_descript = ["Gene Expression"] * (len(seq_files) // 2)

    return fq_files, names, lib_descript


@app.command()
def demux() -> None:
    """Create a job file to perform demultiplexing with Cellranger bcl2fastq
    NOTE! This is currently non-functional!
    
    This script assumes that the project is organized according to the `scrna-processor
    cookiecutter <https://gitlab.com/guthridge_informatics/scrna-processor>`_\b

    """
    pass


@app.command()
def count(
    project_dir: Path = typer.Argument(
        ...,
        help="Path to the directory containing the project (i.e. `/scratch/myscrnaseqproject/`",
    ),
    job_out: Path = typer.Option(
        f"{home()}/workspace/jobs",
        "--job_out",
        "-f",
        help="Path to which job files should be saved",
    ),
    libraries_out: Optional[Path] = typer.Option(
        None,
        "--library_out",
        "-lo",
        help="Path where the `libraries_{run}.csv` files should be saved",
    ),
    memory: int = typer.Option(
        32, "--mem", "-m", help="Amount of memory to request for the job"
    ),
    cpus: int = typer.Option(
        8, "--cpus", "-c", help="Number of CPUs to request for the job"
    ),
    jobs: int = typer.Option(
        8, "--jobs", "-j", help="Number of simultaneous jobs to start"
    ),
    status: List[StatusMessage] = typer.Option(
        [StatusMessage.END, StatusMessage.FAIL],
        "--status",
        "-s",
        help="Type of status updates to email. Pass the argument multiple times to for multiple statuses.",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help="Email address to which to send status updates",
    ),
    chemistry: Optional[Chemistry] = typer.Option(
        Chemistry.auto, "--chemistry", "-ch", help="Assay configuration."
    ),
    cellranger: str = typer.Option(
        "/Volumes/guth_aci_informatics/software/cellranger-5.0.0",
        "--cellranger",
        "-cr",
        help="Path to the cellranger folder.",
    ),
    transcriptome: str = typer.Option(
        "/Volumes/guth_aci_informatics/references/genomic/chimeras/indices/refdata-gex-GRCh38_and_mm10-2020-A",
        help="Path to the STAR indices that were either downloaded from 10x Genomics or generated using `cellranger mkref`",
    ),
) -> None:
    """Quickly create a job file to perform counting with 10X's Cellranger

    This script assumes that the project is organized according to the `scrna-processor
    cookiecutter <https://gitlab.com/guthridge_informatics/scrna-processor>`_\b

    """

    project_dir = Path(project_dir)
    if job_out is None:
        job_out = project_dir.joinpath("scripts")
    else:
        job_out = Path(job_out)
    if libraries_out is None:
        libraries_out = project_dir.joinpath("metadata")
    else:
        libraries_out = Path(libraries_out)

    data_dir = project_dir.joinpath("data")
    fastqs_dir = data_dir.joinpath("fastqs")

    fastq_subdirs = [_ for _ in fastqs_dir.iterdir() if _.is_dir()]
    runs = [_.name for _ in fastq_subdirs]

    status = ",".join(status)

    logger.info(f"Processing the following runs: {runs}")

    for subdir in fastq_subdirs:
        fastq_files = []
        sample_names = []
        library_types = []

        adt_subdir = subdir.joinpath("adt")
        gex_subdir = subdir.joinpath("gex")
        hto_subdir = subdir.joinpath("hto")

        if adt_subdir.exists():
            x, y, z = extract_subdir_files(
                subdir=subdir.joinpath("adt"), libtype="adt"
            )
            fastq_files = np.concatenate([fastq_files, x]).flat
            sample_names = np.concatenate([sample_names, y]).flat
            library_types = np.concatenate([library_types, z]).flat

        if gex_subdir.exists():
            x, y, z = extract_subdir_files(
                subdir=subdir.joinpath("gex"), libtype="gex"
            )
            fastq_files = np.concatenate([fastq_files, x]).flat
            sample_names = np.concatenate([sample_names, y]).flat
            library_types = np.concatenate([library_types, z]).flat

        if hto_subdir.exists():
            x, y, z = extract_subdir_files(
                subdir=subdir.joinpath("hto"), libtype="hto"
            )
            fastq_files = np.concatenate([fastq_files, x]).flat
            sample_names = np.concatenate([sample_names, y]).flat
            library_types = np.concatenate([library_types, z]).flat

        library_csv_file = libraries_out.joinpath(f"libraries_{subdir.name}")
        logger.info(f"writing library file to {library_csv_file}")
        pd.DataFrame(
            data={
                "fastqs": list(fastq_files),
                "sample": sample_names,
                "library_type": library_types,
            }
        ).to_csv(
            path_or_buf=f"{library_csv_file}.csv",
            sep=",",
            index=False,
        )

    for run in runs:
        # Start writing to this file
        jobscript = (
            f"#! /bin/bash -l\n"
            f"#SBATCH -J {run}\n"
            f"#SBATCH -o count_{run}.log\n"
        )

        if email is not None:
            jobscript = (
                f"{jobscript}"
                f"#SBATCH --mail-user={email}\n"
                f"#SBATCH --mail-type={status}\n"
            )

        jobscript = (
            f"{jobscript}"
            f"#SBATCH --mem={memory}G\n"
            f"#SBATCH --partition=serial\n"
            f"#SBATCH --nodes=1\n"
            f"#SBATCH --cpus-per-task={cpus}\n"
            f"\n"
            f"export _JAVA_OPTIONS='-Xmx{memory}G -Xms4G -XX:+UseParallelGC -XX:ParallelGCThreads={cpus}'\n"
            f"export PATH={cellranger}:$PATH\n"
            f"\n"
            f"cellranger count \\\n"
            f"\t--id {run} \\\n"
            f"\t--transcriptome {transcriptome} \\\n"
            f"\t--libraries {project_dir}/metadata/libraries_{run}.csv \\\n"
            f"\t--feature-ref {project_dir}/metadata/feature-barcodes.csv \\\n"
            f"\t--jobmode slurm \\\n"
            f"\t--maxjobs {jobs} \\\n"
            f"\t--chemistry {chemistry} \\\n"
            f"\t--mempercore {int(memory/jobs)} \\\n"
            f"\t--jobinterval 2000 \\\n"
            f"\t--uiport 3838 \\\n"
            f"\t--no-bam \\\n"
            f"\t--include-introns\n"
        )

        output_jobscript = Path(job_out, f"{run}_counts.job")
        logger.info(jobscript)
        logger.info(f"Writing jobscript to {output_jobscript.resolve()}")

        with output_jobscript.open("w") as f:
            f.writelines(jobscript)


if __name__ == "__main__":
    app()
