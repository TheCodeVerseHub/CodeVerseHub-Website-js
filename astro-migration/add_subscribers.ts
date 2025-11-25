import { db } from './src/db';
import { sql } from 'drizzle-orm';

async function main() {
  try {
    db.run(sql`
      CREATE TABLE IF NOT EXISTS subscribers (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        email text NOT NULL UNIQUE,
        is_active integer DEFAULT true,
        created_at integer NOT NULL
      );
    `);
    console.log('Subscribers table created successfully');
  } catch (e) {
    console.error(e);
  }
}

main();
