# CodeVerseHub - Discord Community Website

A modern and performant website built with Astro for the CodeVerseHub Discord community. Our platform showcases community events, contests, resources, and member achievements.

## Features

### Core Features
- **Modern Stack**: Built with Astro, React, and Tailwind CSS for optimal performance
- **Hybrid Rendering**: SSR + static generation for the best of both worlds
- **Community Hub**: Showcase upcoming events, contests, and community achievements
- **Resource Library**: Curated programming resources and learning materials
- **Interactive UI**: Dynamic components with seamless navigation
- **Dark Mode**: Full dark mode support with system preference detection

### Key Pages
- **Home**: Community overview and latest updates
- **About**: Our mission and community values
- **Events**: Upcoming coding contests and community events
- **Resources**: Programming guides and learning materials
- **Timeline**: Community milestones and achievements
- **FAQ**: Common questions and answers

### Developer Features
- **Type Safety**: Full TypeScript support
- **Component Reuse**: Mix of Astro and React components
- **Performance**: Optimized assets and minimal JS
- **SEO Ready**: Built-in SEO optimization tools
- **Analytics**: Privacy-focused analytics integration

##  Technology Stack

- **Framework**: Astro 4.16.19
- **UI Components**: React 18
- **Styling**: Tailwind CSS
- **Database**: SQLite with Drizzle ORM
- **Type Safety**: TypeScript
- **Deployment**: Netlify/Vercel

##  Project Structure

```
cvh/
├── astro-migration/      # Migration-related scripts and docs
├── public/               # Static assets (images, fonts)
├── src/                  # Source code
│   ├── components/       # Reusable UI components (React/Astro)
│   ├── layouts/          # Page layouts
│   ├── pages/            # Site pages and API endpoints
│   ├── styles/           # Global and component styles
│   └── db/               # Drizzle ORM schema and seed
├── package.json          # Project dependencies
├── astro.config.mjs      # Astro configuration
├── tsconfig.json         # TypeScript configuration
└── README.md             # This file
```

##  Quick Start

### Prerequisites
- Node.js 18 or higher
- npm or pnpm
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd codeversehub
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Set up the database**
   ```bash
   npm run db:generate
   npm run db:push
   npm run db:seed
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open the application**
   - Visit http://localhost:3000 in your browser

## 📊 Development

### Environment Setup

Create a `.env` file in the root directory:
```bash
# Database
DATABASE_URL=file:./data.db

# Site Configuration
PUBLIC_SITE_URL=http://localhost:3000
PUBLIC_SITE_NAME=CodeVerseHub

# Optional: Analytics
PUBLIC_UMAMI_WEBSITE_ID=your-umami-id
PUBLIC_UMAMI_URL=your-umami-url
```

### Database Management

The project uses Drizzle ORM with SQLite:

```bash
# Generate migrations
npm run db:generate

# Apply migrations
npm run db:push

# Seed database
npm run db:seed
```

### Type Safety

The project uses TypeScript for type safety:

- All components are fully typed
- Database schema is type-safe with Drizzle
- Props validation throughout
- Type-safe environment variables

### Component Development

- Use Astro components for static content
- React components for interactive features
- Tailwind for consistent styling
- Leverage Astro's partial hydration

## 📱 Development Features

### Performance
- Automatic image optimization
- CSS/JS minification
- Partial hydration
- Responsive images
- Lazy loading

### SEO
- Built-in meta tags
- OpenGraph support
- Sitemap generation
- robots.txt configuration
- Structured data

### Accessibility
- ARIA attributes
- Keyboard navigation
- Color contrast compliance
- Screen reader support
- Focus management

### Analytics
- Privacy-focused analytics
- Page view tracking
- Performance monitoring
- User journey analysis
- Custom events

##  Future Enhancements

- Real-time chat integration
- Discord bot integration
- Member achievements system
- Event registration system
- Resource rating system
- Community blog

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and build
5. Submit a pull request

##  License

This project is built for educational purposes and community use.

##  Support

For support and questions:
- Visit our Discord server
- Check the FAQ page
- Open an issue in the repository

##  Changelog

### Version 2.0.0 (October 2025)
- Complete migration to Astro
- New modern design system
- Improved performance metrics
- Enhanced SEO optimization
- Dark mode support
- Mobile responsiveness

---

**CodeVerseHub** - Built with Astro 🚀 for the programming community

---

## 🚀 Deployment


The website can be deployed to either Netlify or Vercel for optimal performance.

### Netlify Deployment

1. **Connect your repository**
   - Connect your GitHub repository to Netlify
   - Select the repository and branch to deploy

2. **Configure build settings**
   ```bash
   Build command: npm run build
   Publish directory: dist
   Node version: 18.x
   ```

3. **Environment variables**
   ```
   DATABASE_URL=file:../data.db
   PUBLIC_SITE_URL=your-site-url
   ```

4. **Deploy**
   - Trigger deploy from Netlify dashboard
   - Site will be live at `your-site.netlify.app`

### Vercel Deployment

1. **Import your repository**
   - Connect your GitHub repository to Vercel
   - Import the project

2. **Configure project**
   ```bash
   Framework Preset: Astro
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

3. **Environment setup**
   - Add the same environment variables as Netlify
   - Configure any additional settings

4. **Deploy**
   - Trigger deployment
   - Site will be live at `your-project.vercel.app`

### Deployment Notes

- **Database**: The SQLite database is included in the deployment
- **Assets**: Static assets are optimized during build
- **Performance**: Both platforms provide global CDN
- **SSL**: Automatic HTTPS certificates
- **Analytics**: Built-in deployment analytics
- **Continuous Deployment**: Automatic deployments on push

---

### Development vs Production

For local development:
```bash
# Development server
npm run dev

# Production build
npm run build
npm run preview
```
