# Concurrent Execution with `concurrently`

This project uses [concurrently](https://www.npmjs.com/package/concurrently) to run multiple commands simultaneously. This is particularly useful for running both the frontend (React) and backend (FastAPI) development servers in a single terminal window.

## What is `concurrently`?

`concurrently` is an NPM package that allows you to run multiple commands concurrently (at the same time). It handles the output from all commands, prefixing them so you can distinguish which process produced which log line. It also manages the lifecycle of these processes, allowing you to kill all of them with a single `Ctrl+C`.

## How We Use It

In the root `package.json`, we have defined the following scripts:

```json
"scripts": {
  "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
  "dev:backend": "cd backend && make run",
  "dev:frontend": "cd frontend && npm run dev"
}
```

### Breakdown

1.  **`dev:backend`**: Navigates to the `backend` directory and runs `make run`, which starts the FastAPI server using Uvicorn.
2.  **`dev:frontend`**: Navigates to the `frontend` directory and runs `npm run dev`, which starts the Vite development server.
3.  **`dev`**: This is the main command. It uses `concurrently` to execute both `dev:backend` and `dev:frontend` in parallel.

## Benefits

*   **Single Command**: You only need to run `npm run dev` to start the entire application stack.
*   **Unified Output**: Logs from both the frontend and backend appear in the same terminal, making it easier to spot integration issues.
*   **Simplified Workflow**: No need to open multiple terminal tabs or windows.

## Usage

To start the application:

```bash
npm run dev
```

This will start:
*   Frontend at `http://localhost:5173`
*   Backend at `http://localhost:8000`
