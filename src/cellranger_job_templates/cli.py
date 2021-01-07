"""Console script for cellranger_job_templates."""
import sys
import click
from os.path import join

from typing import List, Optional
from .cellranger_job_templates import get_userhome

@click.group()
def main():
    pass

@main.command()
# @click.argument("runs", required=True)
@click.option(
    "--runs",
    #  required=True,
     type=str
     )
@click.option(
    "--file_dir",
    "-f",
    help="path of where to write job files to",
    type=str,
    default=get_userhome(),
    show_default=True,
)
@click.option(
    "--memory",
    "-m",
    help="amount of memory to request for the job",
    type=int,
    default=32,
    show_default=True,
)
@click.option(
    "--cpus",
    "-c",
    help="number of cpus to request",
    type=int,
    default=8,
    show_default=True,
)
@click.option(
    "--jobs",
    "-j",
    help="number of cpus to request",
    type=int,
    default=8,
    show_default=True,
)
@click.option(
    "--jobs",
    "-j",
    help="number of cpus to request",
    type=int,
    default=8,
    show_default=True,
)
@click.option(
    "--email",
    "-e",
    help="email address to which to send status updates",
    type=str,
    default=None,
    show_default=True,
)
@click.option(
    "--status",
    "-s",
    help="type of status updates to send",
    type=click.Choice(["END","FAIL","START"]),
    default=["END","FAIL"],
    multiple=True,
    show_default=True,
)
@click.option(
    "--cellranger",
    help="path to where cellranger is installed",
    type=str,
    default="/Volumes/guth_aci_informatics/software/cellranger-5.0.0",
    show_default=True,
)
@click.option(
    "--transcriptome",
    help="path to where cellranger is installed",
    type=str,
    default="/Volumes/guth_aci_informatics/references/genomic/chimeras/indices/refdata-gex-GRCh38_and_mm10-2020-A",
    show_default=True,
)
@click.option(
    "--project_path",
    "-p",
    help="full path to project",
    type=str,
    default="/s/guth-aci",
    show_default=True,
)
@click.help_option(show_default=True)
def count(
    runs: List[str],
    file_dir: str = f"{get_userhome()}/workspace/jobs",
    memory: int = 128,
    cpus: int = 8,
    jobs: int = 8,
    email: Optional[str] = None,
    status: List[str] = ["END","FAIL"],
    cellranger: str = "/Volumes/guth_aci_informatics/software/cellranger-5.0.0",
    transcriptome: str = "/Volumes/guth_aci_informatics/references/genomic/chimeras/indices/refdata-gex-GRCh38_and_mm10-2020-A",
    project_path: str = "/s/guth-aci",
    ) -> None:
    """Quickly create a job file to perform counting with 10X's Cellranger

    This script assumes that the project is organized according to the 
    [scrna-processor cookiecutter](guthridge_informatics/scrna-processor)

    \b
    Parameters:
    -----------
    runs:
        A list of folders within your PROJECT/data/fastqs directory that you
        wish to process.  The runs should be separated with commas.

    """
    runs = runs.split(",")
    status = ",".join(status)

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
            f"#SBATCH --mem={memory}\n"
            f"#SBATCH --partition=serial\n"
            f"#SBATCH --nodes=1\n"
            f"#SBATCH --cpus-per-task={cpus}\n"
            f"\n"
            f"export _JAVA_OPTIONS='-Xmx{memory}G -Xms4G -XX:+UseParallelGC -XX:ParallelGCThreads={cpus}'\n"
            f"export PATH={cellranger}:$PATH\n"
            f"\n"
            f"cellranger count \\\n"
            f"\t--id={run} \\\n"
            f"\t--transcriptome={transcriptome} \\\n"
            f"\t--libraries={project_path}/metadata/libraries-{run}.csv \\\n"
            f"\t--feature-ref={project_path}/metadata/feature-barcodes.csv \\\n"
            f"\t--jobmode=slurm \\\n"
            f"\t--maxjobs={jobs} \\\n"
            f"\t--mempercore={int(memory/jobs)} \\\n"
            f"\t--jobinterval=2000 \\\n"
            f"\t--uiport=3838 \\\n"
            f"\t--no-bam \\\n"
            f"\t--include-introns\n"
        )
        
        with open(join(file_dir, f"{run}_counts.job"), "w") as f:
            f.writelines(jobscript)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
