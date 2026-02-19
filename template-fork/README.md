# [Project Name]

> One-line description of what this does.

## Stack

- React 19 + Vite
- Radix UI (no Tailwind)
- TanStack Router
- Vitest + Testing Library
- Docker ready

## Getting Started

```bash
nvm use 22
pnpm install
make dev
```

## Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start dev server |
| `make build` | Production build |
| `make test` | Run tests |
| `make docker-build` | Build Docker image |

## Environment Variables

Copy `.env.example` to `.env` and fill in values.

## Project Structure

```
src/
  components/   # Reusable UI components (Radix UI)
  pages/        # Route pages (TanStack Router)
  hooks/        # Custom hooks
  lib/          # Utilities and API clients
  styles/       # Global styles
```

## Conventions

See `.cursor/rules/main.mdc` for full coding conventions.

## License

MIT
