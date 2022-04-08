# Contributing to notion-wrapper

🙌 Firstly, thanks for taking the time to contribute! 🙌

The following are the set of guidelines for contributing towards this repository on Github. These are mostly guidelines
, not rules. Use your best judgement, and feel free to propose changes to this project in a pull request.

## Code Contribution

## 1. Where to start from?

If you've noticed a bug or have a question, then kindly [search the issue tracker][tracker] to see if someone
else has already created a ticket. If not, go ahead and [add one][new issue]!

## 2. Want to fix an issue or add a new feature?

If this is something you think you can fix, then follow the following steps:

### Step 1: Discuss

Before jumping on any ticket or any feature which you think should be there in the framework, discuss with me on my [site][] or email me @ dsouzasunny1436@gmail.com. Once you get go-ahead, you can proceed by following the steps mentioned hereafter.

### Step 2: Setup your E-mail in Git

Assuming you have already done this. But if you are new and may forget this, you can do it as described [here][setup].

### Step 3: Fork and clone the repository

To Fork and clone the repository, see this useful [post][fork].

### Step 4: Create new Branch

Now create a new branch with a descriptive name in your forked repo. Refer [here][branch] to know about Git branches.

### Step 5: Commit with a descriptive message

If committing a fix for a ticket, always start with `Fixed #[Ticket ID]` than describe the changes in detail.
For an example on how to write a proper commit message, see [this][commitHelp] post.

### Step 6: Push changes to your cloned fork

After committing the changes, you need to push the commit to your cloned repo by executing `git push origin your-branch-name` command in the terminal.

### Step 7: Send Pull Request

Sending Pull Request will be the last step of your contribution. To know how to raise a Pull Request, see [this][pr] post.

> **NOTE:** From your second contribution onwards, you can skip steps **(1) and (2)**.

## Process and Guidelines

There is a process in place to help maintain the quality of the framework. To adhere to this process, some coding standards and CI pipelines are defined along with static code analysis. The same are detailed below:

### Git workflow

Since the repository is hosted on GitHub, it has been configured to only accept **signed commits** from any
contributor (_including me :wink:_). So make sure to **sign your commits** before sending Pull Request, **else the
PR will be rejected**. To know more about signed commits, check out this [post][sign-commit].

### Branching strategy

Specific Branching strategy has been defined on this project where **NO COMMITS** are done directly into `main` or `master` branch.

There are 3 main branches:
- `develop`: All feature branches will be merged into this branch after `Pull Request` review.
- `release`: When `develop` branch is clean and all CI tests are **green**, then `develop` branch will be merged into this branch via `Pull Request`. After merge, a `beta` release of version would published to Maven central.
- `main` or `master`: After successful Beta testing, `release` branch will then be merged into `master` via `Pull Request`. After merge, final release version cut would published to Maven central.

### Working on open tickets

Any work being done on any open tickets, should be done in a new branch with naming pattern `issue-<ticket no>` created from `develop` branch.

### Pull Request pre-requisites

Any Pull Request raised should make sure following checks are successful:
- Pull Request is raised to merge changes to `develop` branch.
- Commits is GPG signed.
- There is at least one reviewer.
- Github Action tests are green.
- Branch is up to date with `develop` branch.

### Code Styling

There is always a chance of different code styling when many contributors work together on a project.

Make sure to format the code before sending the **Pull Request**.

### Test coverage

For assuring quality of framework to prospective users, test coverage plays an important role. That's why a benchmark of **80% or more** is set to be required for overall test coverage on this project. It is advisable to add unit tests for any new code which is being added.

[comment]: <> (### SonarCloud Code Quality monitoring)

[comment]: <> (For each commit to any of the branches described above, CI will also execute static code analysis.)

## Issues and Suggestions.

If you find any issue in the framework or you have any suggestions for enhancement, please feel free to raise a ticket for it. Together we can make the framework even more effective and easy for other Test Engineers to use it in their daily automation tasks.

[sign-commit]: https://help.github.com/en/articles/signing-commits
[fork]: https://help.github.com/articles/fork-a-repo/
[branch]: https://www.atlassian.com/git/tutorials/using-branches
[setup]: https://help.github.com/articles/setting-your-commit-email-address-in-git
[commitHelp]: https://github.com/erlang/otp/wiki/Writing-good-commit-messages
[pr]: https://help.github.com/articles/creating-a-pull-request
[site]: https://sunnydsouza.com