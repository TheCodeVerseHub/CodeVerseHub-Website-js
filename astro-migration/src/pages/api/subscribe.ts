import type { APIRoute } from 'astro';
import { db } from '../../db';
import { subscribers } from '../../db/schema';
import { z } from 'zod';

const subscribeSchema = z.object({
  email: z.string().email(),
});

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const data = subscribeSchema.parse(body);
    
    await db.insert(subscribers).values({
      email: data.email,
    });
    
    return new Response(JSON.stringify({ success: true, message: 'Subscribed successfully!' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    // Check for unique constraint violation
    if (error instanceof Error && error.message.includes('UNIQUE constraint failed')) {
        return new Response(JSON.stringify({ error: 'Email already subscribed' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    return new Response(JSON.stringify({ error: 'Invalid request' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
