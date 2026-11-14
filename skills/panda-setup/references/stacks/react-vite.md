# React + TypeScript + Vite

Sources to check at setup time: [Vite getting started](https://vite.dev/guide/)
(Node requirement and `create-vite` templates), [React docs](https://react.dev/),
[Vitest guide](https://vitest.dev/guide/), and [Testing Library](https://testing-library.com/docs/react-testing-library/intro/).
Confirm with `npm view vite version engines` and `npm create vite@latest -- --help`.

## Generator

```sh
npm create vite@latest <dir> -- --template react-ts --no-interactive
```

Read `--help` first: flags and default linters change between releases.
`create-vite` has an option that removes existing files in a non-empty target;
never use it on a user's directory. Generate into an empty directory, or into a
temporary directory and merge selected files when adapting an existing repo.
Use the project's package manager (`pnpm create`, `yarn create`, `bun create`).

## Structure and tests

Keep the template's `src/` layout, `index.html`, and tsconfig split. Replace
demo content only when the user describes the initial page. The template may not
include a test runner; when meaningful tests are required, add Vitest with jsdom
and Testing Library and configure `test.environment` in the Vite config using
the documented `vitest/config` helper. A real test renders a component and
asserts behavior (for example, clicking changes visible state).

## Commands

Use the generated scripts and record them exactly (`dev`, `build` which also
type-checks, `lint`, `preview`), plus the added `test` script. Smoke: build,
run `preview` on a free port with a strict port option, and request `/`.
For an API backend, prefer the Vite dev server `server.proxy` over hard-coded
cross-origin URLs, and document it.

Generators write their own `.gitignore`; reconcile it with the root one in a
combined repository. Ignore `node_modules/`, `dist/`, `.env.local`; track the lockfile.
