# Frontend - E-commerce Data Generation Platform

React frontend application built with Vite and Tailwind CSS.

## Tech Stack

- **React 19.2.0** - UI library
- **Vite 4.5.0** - Build tool and dev server
- **Tailwind CSS 3.3.5** - Utility-first CSS framework
- **React Router DOM 6.8.0** - Client-side routing
- **Zustand 5.0.9** - State management
- **SignalR 8.0.0** - Real-time communication
- **jwt-decode 4.0.0** - JWT token decoding

## Available Scripts

### `npm run dev`

Runs the app in development mode with Vite dev server.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will hot-reload when you make changes.\
You may also see lint errors in the console.

### `npm test`

Launches the test runner in watch mode.\
Uses React Testing Library and Jest for testing.

### `npm run build`

Builds the app for production to the `dist` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include hashes.\
Your app is ready to be deployed!

### `npm run preview`

Locally preview the production build.\
Useful for testing the production build before deployment.

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   │   ├── Layout.jsx
│   │   ├── HomePage.jsx
│   │   ├── DataTablePage.jsx
│   │   └── PrivateRoute.jsx
│   ├── stores/          # Zustand state stores
│   │   ├── authStore.js
│   │   └── dataStore.js
│   ├── services/        # API service functions
│   │   └── api.js
│   ├── config/          # Configuration
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Utility functions
│   ├── icons/           # Icon components
│   ├── App.jsx          # Main application component
│   └── index.jsx        # Application entry point
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── package.json         # Dependencies and scripts
```

## Key Features

- **Authentication**: Login/register with JWT token management
- **Protected Routes**: Route guards for authenticated users
- **Data Generation**: Interface for generating e-commerce data
- **Real-time Updates**: SignalR integration for job notifications
- **Data Tables**: View generated data across multiple tables
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS

## Development

### Prerequisites

- Node.js 14 or higher
- npm or yarn

### Setup

1. Install dependencies:
```bash
npm install
```

2. Configure API endpoint in `src/config` if needed

3. Start development server:
```bash
npm run dev
```

### Environment Variables

Create `.env` file if needed:

```env
VITE_API_BASE_URL=http://localhost:5000
```

Access in code:
```javascript
const apiUrl = import.meta.env.VITE_API_BASE_URL;
```

## Building for Production

1. Build the project:
```bash
npm run build
```

2. Preview the build locally:
```bash
npm run preview
```

3. Deploy the `dist` folder to your hosting service

## Learn More

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

For complete project documentation, see the main [README.md](../README.md) in the root directory.
