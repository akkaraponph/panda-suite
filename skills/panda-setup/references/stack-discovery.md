# Setting up any stack

Use this procedure for every language, framework, and runtime: Rust, Java,
.NET, Ruby, PHP, Elixir, mobile, desktop, CLI tools, or anything else. The
optional [stack notes](stacks/) record pitfalls already observed for some
stacks; they supplement this procedure and never replace current research.

## 1. Identify the stack precisely

From the request and repository, name each application's language, runtime,
framework, package manager, and build tool. If the user names only a goal
("a REST API", "a web dashboard"), recommend one stack in plain terms with a
short reason, offer one alternative, and continue with the recommendation
unless the choice materially changes the project.

## 2. Find the official setup path

Locate primary sources for each component: the official "getting started" or
installation page, the release or version-support page, the official
generator or project template (if any), and the package registry entry. Use
the ecosystem's own tooling to confirm facts locally, for example:

- generator help: `<generator> --help`
- registry metadata: `npm view`, `go list -m`, PyPI JSON, `cargo search`,
  `gem info -r`, Maven Central, NuGet, Hex, Packagist, pub.dev
- installed toolchain: `<tool> --version`

Record, for each component, the six facts in
[discovery and versions](discovery-and-versions.md): runtime support, release
status, compatibility, official install/scaffold command, directory
conventions, and available dev/build/test/type-check/lint commands.

## 3. Inspect the generator before running it

Read its help and docs for: interactive prompts and the flags that answer them,
behavior on a non-empty directory (refuse, merge, or delete), whether it creates
a nested Git repository, installs dependencies, writes agent instruction files
or ignore files, sends telemetry, or reuses saved local preferences. Pass every
consequential choice explicitly. In a non-empty directory, generate into a
temporary directory and merge without replacing existing files.

If no official generator exists, write the minimal files the official docs show.

## 4. Make tests meaningful

Many templates ship without a test runner or with only a placeholder test. Use
the test approach the framework's docs recommend, and add one test that
exercises real behavior (a request to an endpoint, a rendered component
interaction, a command's output). Prefer in-process testing utilities over
starting a server when the framework provides them.

## 5. Verify from a clean state

Run each documented command once as written. Then remove generated build
output and caches (not dependencies the lockfile restores) and rerun the
build, type check, and tests, because some checks depend on artifacts that a
fresh clone lacks. Start the application on a free port, exercise it, and stop it.

## 6. Know when to stop

Proceed when official sources cover installation or scaffolding, a run command,
and a test or check command, and those commands work locally. If evidence is
missing or contradictory, report the specific gap with the sources consulted
and the question that would resolve it. Write any new pitfalls you confirmed
into the final report so they can become a stack note later.
