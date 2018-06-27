# Development Guide

Maintainers guide to the `pytest-requests` package.

## Release Checklist

### PyPi releases

- [ ] Check that build passes on all versions

### Owner Todos:

- [ ] Ensure `CHANGES.rst` is up-to-date.
- [ ] Update `CHANGES.rst`, replacing `master` with release version and date.
- [ ] Bumpversion to `release` (with tag).
- [ ] Bumpversion to `minor`.
- [ ] Push release cycle commits and tag to `origin/master`.
- [ ] Update Read the Docs space.

### Owner/Contributor Todos:

- [ ] Clear dist folder using `rm -f dist/*`
- [ ] From *release tag*, build using `python setup.py sdist bdist_wheel` and publish to PyPI (using `twine upload dist/*`).
- [ ] Tell a friend
