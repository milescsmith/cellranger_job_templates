=========================
cellranger_job_templates
=========================


.. image:: https://img.shields.io/pypi/v/cellranger_job_templates.svg
        :target: https://pypi.python.org/pypi/cellranger_job_templates

.. image:: https://img.shields.io/travis/milescsmith/cellranger_job_templates.svg
        :target: https://travis-ci.com/milescsmith/cellranger_job_templates

.. image:: https://readthedocs.org/projects/cellranger-count-template/badge/?version=latest
        :target: https://cellranger-count-template.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Generate SLURM job scripts for 10x Genomics' Cellranger pipeline


* Free software: BSD license
* Documentation: https://cellranger-count-template.readthedocs.io.


Usage
--------

.. code-block:: console

        Usage: cjt [OPTIONS] COMMAND [ARGS]...

        Options:
        --install-completion [bash|zsh|fish|powershell|pwsh]
                                        Install completion for the specified shell.
        --show-completion [bash|zsh|fish|powershell|pwsh]
                                        Show completion for the specified shell, to
                                        copy it or customize the installation.

        --help                          Show this message and exit.

        Commands:
        count  Quickly create a job file to perform counting with 10X's
                Cellranger...

        demux  Create a job file to perform demultiplexing with Cellranger...

While an interface for all of the Cellranger subcommands is planned, currently only the `count` subcommand is covered.

.. code-block:: console

        Usage: cjt count [OPTIONS] PROJECT_DIR

        Quickly create a job file to perform counting with 10X's Cellranger

        This script assumes that the project is organized according to the `scrna-
        processor cookiecutter <https://gitlab.com/guthridge_informatics/scrna-
        processor>`_

        Arguments:
        PROJECT_DIR  Path to the directory containing the project (i.e.
                `/scratch/myscrnaseqproject/`  [required]


        Options:
        -f, --job_out TEXT              Path to which job files should be saved
                                        [default: /home/milo/workspace/jobs]

        -lo, --library_out TEXT         Path where the `libraries_{run}.csv` files
                                        should be saved

        -m, --mem INTEGER               Amount of memory to request for the job
                                        [default: 32]

        -c, --cpus INTEGER              Number of CPUs to request for the job
                                        [default: 8]

        -j, --jobs INTEGER              Number of simultaneous jobs to start
                                        [default: 8]

        -s, --status [END|FAIL|START|NONE|BEGIN|REQUEUE|ALL|INVALID_DEPEND|STAGE_OUT|TIME_LIMIT|TIME_LIMIT_90|TIME_LIMIT_80|TIME_LIMIT_50|ARRAY_TASKS]
                                        Type of status updates to email. Pass the
                                        argument multiple times to for multiple
                                        statuses.  [default: StatusMessage.END,
                                        StatusMessage.FAIL]

        -e, --email TEXT                Email address to which to send status
                                        updates

        -ch, --chemistry [auto|threeprime|fiveprime|SC3Pv1|SC3Pv2|SC3Pv3|SC5P-PE|SC5P-R2|SC-FB]
                                        Assay configuration.  [default: auto]
        -cr, --cellranger TEXT          Path to the cellranger folder.  [default: /V
                                        olumes/guth_aci_informatics/software/cellran
                                        ger-5.0.0]

        --transcriptome TEXT            Path to the STAR indices that were either
                                        downloaded from 10x Genomics or generated
                                        using `cellranger mkref`  [default: /Volumes
                                        /guth_aci_informatics/references/genomic/chi
                                        meras/indices/refdata-gex-
                                        GRCh38_and_mm10-2020-A]

        --help                          Show this message and exit.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
