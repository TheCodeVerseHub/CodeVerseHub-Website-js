import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { testimonials, announcements } from './schema';

async function seed() {
  const sqlite = new Database('data.db');
  const db = drizzle(sqlite);

  // Seed testimonials
  await db.insert(testimonials).values([
  {
    name: 'Alex Chen',
    role: 'Frontend Developer',
    content: 'CodeVerseHub has been instrumental in my growth as a developer. The community is supportive and the challenges are engaging!',
    avatar: '/images/default.jpg',
    rating: 5,
    isActive: true,
  },
  {
    name: 'Sarah Johnson',
    role: 'Backend Engineer',
    content: 'Best Discord community for developers. The help channels are always active and people are genuinely helpful.',
    avatar: '/images/default.jpg',
    rating: 5,
    isActive: true,
  },
  {
    name: 'Mike Rodriguez',
    role: 'Full Stack Dev',
    content: 'The coding contests and events keep me motivated. Great place to network with other developers!',
    avatar: '/images/default.jpg',
    rating: 5,
    isActive: true,
  },
]);

  // Seed announcements
  await db.insert(announcements).values([
    {
      title: 'Weekly Coding Challenge Starts Tomorrow!',
      content: 'Join us for this week\'s coding challenge. Prizes for top 3 submissions!',
      isActive: true,
    },
    {
      title: 'New Resources Channel Launched',
      content: 'Check out our newly curated resources channel with tutorials, articles, and courses.',
      isActive: true,
    },
    {
      title: 'Community Milestone: 500 Members!',
      content: 'Thank you all for making CodeVerseHub an amazing community. Here\'s to many more!',
      isActive: true,
    },
  ]);

  console.log('✅ Database seeded successfully!');
  sqlite.close();
}

seed().catch(console.error);
