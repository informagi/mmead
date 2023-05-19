# DuckDB in MMEAD

## How do we use DuckDB in MMEAD?

[DuckDB](https://duckdb.org) serves as the backend to manage the storage and query functionality provided through MMEAD.

A DuckDB database stores tables for the entity information, as well as the embeddings.

## Move storage location

The data is stored at `${HOME}/.cache/mmead`.

The data is quite large, up to 100GB, so your home directory may not be the best location for it.
You can safely move the directory and create a symbolic link to the new location.
For example:

    mkdir -p /export/data/ir/mmead-data
    mv ${HOME}/.cache/mmead /export/data/ir/mmead-data
    ln -sf /export/data/ir/mmead-data ${HOME}/.cache/mmead

## Upgrade DuckDB version

DuckDB is a [fast evolving](https://github.com/duckdb/duckdb/issues) project, with new and improved 
functionalities being added daily if not hourly. You can check the currently installed version:

    pip show duckdb

DuckDB has not yet reached a stable storage format yet, that will be fixed on release `1.0`. 
You will probably want to upgrade DuckDB to a new release, given its fast development, but without 
reimporting all the MMEAD datasets (which takes a fair amount of time).

You can upgrade DuckDB independently of MMEAD, as long as you take care of the following steps.
Let's assume you upgrade from `v0.7.2` to `v0.8.0`.

First, export the MMEAD database (adapt the path name; and note that DuckDB will overwrite any data in that directory):

```Python3
>>> from mmead.util import _get_cursor
>>> cursor = _get_cursor()
>>> cursor.execute("EXPORT DATABASE '/export/data/ir/mmead-data-export' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000)");
```

Next, upgrade DuckDB:

    pip install duckdb==v0.8.0

Using Parquet row groups in the data export still triggers a minor bug, that we work around as follows:

    sed -i -e 's/ROW_GROUP_SIZE [0-9]\+, //g' /export/data/ir/mmead-data-export/load.sql

Remove the old database (or make a backup copy, to be sure):

    rm ${HOME}/.cache/mmead/mmead.db

Finally, import the data into a newly created database:

```Python3
>>> from mmead.util import _get_cursor
>>> cursor = _get_cursor()
>>> cursor.execute("IMPORT DATABASE '/export/data/ir/mmead-data-export'");
```

Import and export take a while, especially if you use the compressed Parquet format as in the example.
For alternative export data formats, refer to DuckDB's 
[import &amp; export](https://duckdb.org/docs/sql/statements/export.html) documentation.


