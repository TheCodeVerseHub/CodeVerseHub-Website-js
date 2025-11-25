# CodeVerseHub - Astro Migration

Migrated from Django to Astro for better performance, less code, and modern developer experience.

## Tech Stack

- **Astro** - Static site generator with islands architecture
- **React** - For interactive components (only where needed)
- **Drizzle ORM** - Lightweight, type-safe database ORM
- **SQLite** - Simple, file-based database
- **TypeScript** - Type-safe development

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install

# Generate database schema
npx drizzle-kit generate
npx drizzle-kit push

# Start development server
npm run dev
```

Visit `http://localhost:3000`

### Build for Production

```bash
# Build static site
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
astro-migration/
├── src/
│   ├── db/           # Database schema & connection
│   ├── layouts/      # Page layouts
│   ├── pages/        # Route pages & API endpoints
│   └── styles/       # Global CSS
├── public/           # Static assets (images, favicon)
├── drizzle/          # Database migrations
└── data.db           # SQLite database file
```

## Features

- ✅ Server-side rendering (SSR)
- ✅ Static page generation
- ✅ API routes for forms
- ✅ Type-safe database queries
- ✅ Zero-config deployment
- ✅ Automatic code splitting
- ✅ Optimized images

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

## Environment Variables

Create `.env` file:

```env
DATABASE_URL="file:./dev.db"
```

## Migration from Django

This project was migrated from Django with these changes:

- Django templates → Astro components
- Django ORM → Drizzle ORM
- Django views → Astro pages/API routes
- manage.py commands → npm scripts
- Render deployment → Vercel/Netlify

## API Routes

- `POST /api/contact` - Submit contact form

## Database Seeding

To add initial testimonials/announcements:

```typescript
// src/scripts/seed.ts
import { db } from './db';
import { testimonials } from './db/schema';

await db.insert(testimonials).values([
  {
    name: 'John Doe',
    role: 'Full Stack Developer',
    content: 'Amazing community!',
    rating: 5,
    isActive: true
  }
]);
```

Run: `tsx src/scripts/seed.ts`

## License

MIT
