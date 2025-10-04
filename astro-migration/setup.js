#!/usr/bin/env node

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import Database from 'better-sqlite3';

console.log('🚀 Setting up CodeVerseHub Astro...\n');

function run(command, description) {
  console.log(`📦 ${description}...`);
  try {
    execSync(command, { stdio: 'inherit' });
    console.log(`✅ ${description} complete\n`);
  } catch (error) {
    console.error(`❌ ${description} failed`);
    process.exit(1);
  }
}

// Check if node_modules exists
if (!fs.existsSync('node_modules')) {
  run('npm install', 'Installing dependencies');
}

// Create .env if it doesn't exist
if (!fs.existsSync('.env')) {
  console.log('📝 Creating .env file...');
  fs.copyFileSync('.env.example', '.env');
  console.log('✅ .env created\n');
}

// Setup database
run('npm run db:generate', 'Generating database schema');

// Apply schema manually since drizzle-kit push has issues
console.log('📦 Creating database tables...');
try {
  const db = new Database('data.db');
  
  // Read and execute the generated SQL
  const sqlPath = './drizzle/0000_perfect_strong_guy.sql';
  if (fs.existsSync(sqlPath)) {
    const sql = fs.readFileSync(sqlPath, 'utf8');
    db.exec(sql);
    console.log('✅ Database tables created\n');
  }
  
  // Check if database has data
  const result = db.prepare('SELECT COUNT(*) as count FROM testimonials').get();
  
  if (result.count === 0) {
    db.close();
    run('npm run db:seed', 'Seeding database with sample data');
  } else {
    db.close();
    console.log('✅ Database already has data\n');
  }
} catch (error) {
  console.error('❌ Database setup failed:', error.message);
  process.exit(1);
}

console.log('\n🎉 Setup complete!\n');
console.log('Next steps:');
console.log('  1. npm run dev     - Start development server');
console.log('  2. npm run build   - Build for production');
console.log('  3. vercel          - Deploy to Vercel\n');
console.log('Visit: http://localhost:3000\n');
