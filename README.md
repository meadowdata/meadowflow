# Meadowflow

- Meadowflow is a proof-of-concept/prototype job scheduler built to explore the idea of
implicit data dependency management.
- Meadowdb (also part of this repo) is a columnar database designed to work with
  Meadowflow
- Meadowgrid (also part of this repo) is a compute layer for running jobs, and should be
  replaced by https://github.com/meadowdata/meadowrun

## Implicit data dependencies

meadowflow and meadowdb work together to capture what data is read and written by which
jobs. This effect system of sorts enables powerful scenarios. For example:

- A job can be scheduled to automatically run whenever its dependencies are updated. In
  a traditional job scheduler, the job definition's dependencies and the actual code's
  data dependencies can get out of sync, which can result in jobs running before their
  dependencies are ready, reading stale data, and thus producing incorrect results.
- Running a regression test on a job or reviewing it for model changes is almost no
  extra work. meadowflow/meadowdb can run a test run of a job with local code changes
  while redirecting all of its outputs to a userspace for comparison.

## Getting started
- See [examples/covid](examples/covid/README.md) for an introduction to meadowdb and
  meadowflow.
- See [examples/covid/regression_test.md](examples/covid/regression_test.md) for a
  deeper dive on regression tests/model change reviews.
- See [readerwriter_shared.py](src/meadowdb/readerwriter_shared.py) for an introduction
  to the meadowdb data layout.
