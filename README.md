# Telegram Marketplace Bot

This project is a simple React application configured to run as a Telegram mini app.

## Scripts

- `npm start` - start the development server.
- `npm run build` - create a production build.
- `npm test` - run tests.
- `npm run lint` - run ESLint on the TypeScript sources.

## Development

Make sure you have Node.js 18 installed. After cloning the repository, install dependencies:

```bash
npm install
```

Then you can start the development server:

```bash
npm start
```
This project contains a simple Telegram bot written in Python along with a React frontend.

## Environment Variables

The bot expects a few environment variables to be set before it can run:

- `TELEGRAM_BOT_TOKEN` – token of your Telegram bot
- `RPC_URL` – Ethereum RPC endpoint used by the wallet utilities

## Running the HTTP Handler

Install Python dependencies and start the handler.

```bash
pip install -r requirements.txt
python -m api.bot
```

This starts an HTTP server that processes Telegram webhook events.

## Starting the React Frontend

Install Node dependencies and start the development server.

```bash
npm install
npm start
```

The application will be available at `http://localhost:3000`.

## Linting and Tests

- Linting: `npx eslint .`
- Tests: `npm test`
