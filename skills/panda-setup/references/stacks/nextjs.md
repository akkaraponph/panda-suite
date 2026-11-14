# Next.js + TypeScript

Sources to check at setup time: [Next.js installation](https://nextjs.org/docs/app/getting-started/installation)
(Node requirement and `create-next-app` options), [project structure](https://nextjs.org/docs/app/getting-started/project-structure),
[testing guides](https://nextjs.org/docs/app/guides/testing), and the
[Next.js blog](https://nextjs.org/blog) for the current major. Confirm with
`npm view next version engines` and `npx create-next-app@latest --help`.

## Generator

Pass every relevant choice explicitly; an option such as `--yes` can reuse
locally saved preferences and make results machine-dependent. Example:

```sh
npx create-next-app@latest <dir> --ts --eslint --app --no-tailwind \
  --no-src-dir --import-alias "@/*" --use-npm --disable-git
```

Choose Tailwind, `src/`, the bundler, and the linter from requirements or team
conventions; use the package manager already in the repository. Use
`--disable-git` inside an existing repository so no nested repository is created.

Check what the generator writes besides the app. Recent versions can create an
`AGENTS.md` with a marked block that the dev server re-adds. Keep that block
intact and add project instructions outside its markers; do not duplicate it in
another host file. Generated ignore files can include a broad `.env*` pattern;
add `!.env.example` (or the project's example file name) and verify it with
`git check-ignore`.

## Structure and tests

Follow the App Router (or the existing Pages Router) conventions; do not add a
separate `src/services` layer by default. Route handlers under `app/api` are
appropriate only when the Next.js app owns that API. No test runner is
included; when tests are needed, follow the official testing guide for the
chosen runner. A smoke check is still required.

## Commands

`dev`, `build`, `start`, `lint` as generated. Generated route types (for
example `LayoutProps`) live in ignored build output, so plain `tsc --noEmit`
can fail on a fresh checkout; generate types first (check the CLI for a
`typegen` command) and document a script such as `next typegen && tsc --noEmit`.
Verify it after deleting `.next/`. The build also type-checks.

If the generator refuses a non-empty destination, scaffold into a temporary
directory and merge without replacing existing files such as the README. Smoke: build, `next start -p <free port>`,
request `/` and check for expected page content, then stop the server.

Ignore `.next/`, `out/`, `node_modules/`, `.env*` except examples, `*.tsbuildinfo`.
Check how the generated `next-env.d.ts` is treated rather than changing it blindly.
