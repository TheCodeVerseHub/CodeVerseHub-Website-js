import { drizzle } from 'drizzle-orm/better-sqlite3';
import Database from 'better-sqlite3';
import * as schema from './schema';

let sqlite;
try {
    // Try to open the database file
    sqlite = new Database('data.db');
} catch (e) {
    console.warn("Failed to open data.db, falling back to in-memory database for build/preview.");
    sqlite = new Database(':memory:');
}

export const db = drizzle(sqlite, { schema });
