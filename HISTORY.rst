=======
History
=======

0.5.0 (2021-03-09)
------------------

* Added:
    * The `count` subcommand now scans the `data/fastq` directory for subdirectories containing fastqs and attempts to generate the library .csv files needed by cellranger count

* Changed:
    * Switched from the `click` to the `typer` library for parsing command line arguments
    * Revamed the cli arguments for the `count` subcommand
    * Updated README.rst

* Removed:
    * Eliminated `setup.py` and fully embraced using `pyproject.toml` and poetry to manage dependencies

0.2.0 (2021-01-07)
------------------

* Changed:
    * `count` is now a command underneath the main function so that
    other template types can be later added.

0.1.0 (2020-12-03)
------------------

* First release
