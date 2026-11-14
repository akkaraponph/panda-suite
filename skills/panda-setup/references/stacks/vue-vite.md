# Vue + TypeScript + Vite

Sources to check at setup time: [Vue quick start](https://vuejs.org/guide/quick-start.html),
[create-vue](https://github.com/vuejs/create-vue), [Vite guide](https://vite.dev/guide/),
and [Vitest guide](https://vitest.dev/guide/). Confirm with `npm view vue version`
and `npm create vue@latest -- --help`.

## Generator

```sh
npm create vue@latest <dir> -- --ts --vitest --eslint
```

Passing feature flags with a directory avoids interactive prompts; check
`--help` for current flags. Add `--router` or `--pinia` only when routing or
shared state is required now. Release-candidate flags are prereleases: do not
use them unless requested. `create-vue` has a force option for non-empty
directories; do not use it on a user's directory.

## Structure and tests

Keep the generated `src/` layout (components, optional `router/` and `stores/`)
and tsconfig files. The Vitest option generates a component test; keep it only
if it tests real behavior and add one for the first real component.

## Commands

Record the generated scripts exactly. Typical ones: `dev`, `build` (type check
plus build), `type-check`, `test:unit`, `lint`, `preview`. Generated lint
scripts can apply fixes (`--fix`); document that, and use the linter without
fix flags for check-only verification. `test:unit` may start watch mode; use
the runner's single-run option in verification and instructions.

Smoke: build, run `preview` on a free port, request `/`. Ignore `node_modules/`,
`dist/`, `.env.local`, lint caches; track the lockfile.
