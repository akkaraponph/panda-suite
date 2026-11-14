# Node.js + TypeScript + Fastify

Sources to check at setup time: [Node.js releases](https://nodejs.org/en/about/previous-releases),
[Fastify documentation](https://fastify.dev/docs/latest/), especially its
[TypeScript guide](https://fastify.dev/docs/latest/Reference/TypeScript/) and
[LTS policy](https://fastify.dev/docs/latest/Reference/LTS/), and the
[TypeScript release notes](https://www.typescriptlang.org/docs/). Confirm with
`npm view fastify version engines` and `npm view <plugin> peerDependencies`.

## Version decisions

- Choose a Node release supported by both Node's release schedule (prefer
  active LTS for new services) and Fastify's LTS table.
- Fastify plugins (`@fastify/*`) track Fastify majors; check each plugin's
  compatibility before adding it. Add plugins only when needed.
- Running `.ts` files directly depends on the installed Node version's type
  stripping support; check the Node docs. If unsupported, use the dev runner the
  Fastify or TypeScript docs recommend rather than inventing one.

## Structure

There is no mandatory generator; a minimal manual setup is usually clearer than
a template. Use the project's package manager (respect `packageManager` and the
existing lockfile).

```text
src/app.ts        build and return the Fastify instance (routes registered)
src/server.ts     read PORT/HOST from env, call listen
src/app.test.ts   tests using app.inject()
```

Separate `buildApp()` from `listen` so tests use `app.inject()` without a port.
Add `routes/` or plugin folders when there is more than a handful of routes.

## Commands

Typical scripts (adapt to the package manager and Node capabilities):

```json
{
  "dev": "node --watch src/server.ts",
  "build": "tsc",
  "typecheck": "tsc --noEmit",
  "test": "node --test src/",
  "start": "node dist/server.js"
}
```

Restrict test discovery to source (or exclude tests from the build output) so
compiled copies are not run twice. Lint only with a configured linter; adding
one is optional. Smoke: build, start on a free port, request the health route.

Ignore: `node_modules/`, `dist/`, `.env`, `*.tsbuildinfo`. Track the lockfile.
