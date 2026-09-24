"""BiCoord-Bench as a package: the tasks are ``bicoord_bench.envs.<task_name>``.

The assets (a few GB) are not part of the package: :func:`bicoord_bench.assets.ensure`
downloads them and sets ``$BICOORD_DATA``, which must happen before importing
``bicoord_bench.envs``.
"""
