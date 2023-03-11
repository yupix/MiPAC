# Contribution guide

Thank you for considering contributing to MiPAC!!!

## Issue

Check the going points before creating an assignment

- To avoid duplicates, please search for similar Issues
- Do not use Issue for questions, etc.
    - We welcome your questions in GitHub Discussion or on the Discord server in the README.


## About Brunch

- `master` is a branch intended for use in a production environment
- `develop` is the branch to work on for the next release
    - If you want to create a pull request, please send it to this branch

## Creating a pull request

- Create an Issue before creating a pull request.
- Please prefix the branch name with a keyword such as `feat` / `fix` / `refactor` / `chore` to identify the pull request as much as possible.  
    - Also, do not include changes other than to resolve the pull request issue
- If you have an Issue that will be resolved by a pull request, please include a link
- Any changes should be described in `CHANGELOG.md`. However, if there is no change from the user's point of view, there is no need to describe it.
- If possible, please use `flake8`, `mypy`, etc. to lint in your local environment.

Thank you for your cooperation.

## Notes

### About the Format

This project uses `axblack` and `isort` formatting. The difference between `axblack` and `black` is whether double or single quotes are used.

### About supported Misskey versions

- Ayuskey v5, 6
- Misskey v13, 12, 11
