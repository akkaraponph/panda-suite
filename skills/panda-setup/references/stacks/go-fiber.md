# Go + Fiber

Sources to check at setup time: [Go release policy](https://go.dev/doc/devel/release),
[Go module layout](https://go.dev/doc/modules/layout),
[Fiber documentation](https://docs.gofiber.io/) and its
[releases](https://github.com/gofiber/fiber/releases). Confirm the latest
stable Fiber major with `go list -m github.com/gofiber/fiber/v<N>@latest` and
read the minimum `go` directive from that module's `go.mod` (module proxy
`https://proxy.golang.org/<module>/@v/<version>.mod`).

## Version decisions

- Fiber majors use different import paths (`/v2`, `/v3`, …) and handler
  signatures. Use the API documented for the selected major; never mix examples
  from different majors. Keep an existing project on its current major.
- The installed Go toolchain must satisfy Fiber's `go` directive. `go mod init`
  writes the local toolchain version; keep or lower it only to what the team supports.

## Structure

Small single service: a root `main.go` is acceptable. Server projects with
non-Go files (frontend, docs, deploy config) benefit from the official layout:
`cmd/<service>/main.go` plus packages under `internal/`. Create packages for
real boundaries only, for example `internal/httpapi` (routes and handlers)
and later `internal/<domain>` when there is domain logic. Do not create
controller/service/repository/interface/DI layers by default; follow an explicit
user preference when given.

Keep an app constructor (`New() *fiber.App`) separate from `Listen`, so tests
can call `app.Test(httptest.NewRequest(...))` without opening a port. Read the
listen address from an environment variable with a local default.

## Commands

```sh
go mod init <module-path>          # ask for the module path if not inferable
go get github.com/gofiber/fiber/v<N>@latest
go mod tidy
gofmt -l .                         # empty output means formatted
go vet ./...
go build ./...
go test ./...
go run ./cmd/<service>
```

Lint beyond `go vet` (for example golangci-lint) only when installed or
requested; do not install it globally unasked. Smoke: run the service on a
free port and request the health route.

Ignore: built binaries (`/bin/` or the binary name), coverage output, `.env`.
Track `go.mod` and `go.sum`.
