const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  ssl: { rejectUnauthorized: false }
});

async function seed() {
  try {
    // 1. Seed conversation
    const conv = await pool.query(`
      INSERT INTO residence_conversations (work_request_id, resident_user_id, worker_user_id, status)
      VALUES (1, 1, 3, 'ACTIVE')
      ON CONFLICT (work_request_id, resident_user_id, worker_user_id) DO UPDATE SET status = 'ACTIVE'
      RETURNING id;
    `);
    const cid = conv.rows[0].id;
    
    // Seed messages
    const msgCheck = await pool.query('SELECT COUNT(*) FROM chat_messages WHERE conversation_id = $1', [cid]);
    if (parseInt(msgCheck.rows[0].count) === 0) {
      await pool.query(`
        INSERT INTO chat_messages (conversation_id, sender_user_id, message_text)
        VALUES 
          ($1, 3, 'Namaste Roshan ji, I am Ashish from AquaPure Tech. I have accepted your sink repair job. I will arrive with the ceramic spindle at 3:30 PM today.'),
          ($1, 1, 'Great, thanks Ashish! Please also check the P-trap seal under the sink granite counter.'),
          ($1, 3, 'Noted. I have the Teflon sealant and 32mm trap ready. See you shortly!');
      `, [cid]);
      console.log('Chat messages seeded for conversation:', cid);
    }

    // 2. Seed work request items
    const itemCheck = await pool.query("SELECT COUNT(*) FROM work_request_items WHERE request_id = 1 AND request_type = 'FLAT_MAINTENANCE'");
    if (parseInt(itemCheck.rows[0].count) === 0) {
      await pool.query(`
        INSERT INTO work_request_items (request_type, request_id, item_name, category, quantity, unit, description)
        VALUES 
          ('FLAT_MAINTENANCE', 1, 'Quarter-turn Ceramic Tap Spindle', 'Plumbing', 1, 'unit', 'For leaking hot/cold kitchen swivel mixer'),
          ('FLAT_MAINTENANCE', 1, 'Heavy Duty 32mm Flexible P-Trap Pipe', 'Plumbing', 1, 'set', 'Under-counter sink basin drain line'),
          ('FLAT_MAINTENANCE', 1, 'PTFE High-Density Thread Seal Tape', 'Plumbing', 2, 'rolls', 'Joint sealing against seepage');
      `);
      console.log('Work items seeded for Request 1');
    }

    // 3. Seed items for society bulk service 1
    const socItemCheck = await pool.query("SELECT COUNT(*) FROM work_request_items WHERE request_id = 1 AND request_type = 'SOCIETY_BULK'");
    if (parseInt(socItemCheck.rows[0].count) === 0) {
      await pool.query(`
        INSERT INTO work_request_items (request_type, request_id, item_name, category, quantity, unit, wing_flat_reference, description)
        VALUES
          ('SOCIETY_BULK', 1, '5-Micron Spun Polypropylene Sediment Cartridge', 'Appliance AMC', 64, 'cartridges', 'Wing A & B', 'Initial particulate pre-filtration replacement'),
          ('SOCIETY_BULK', 1, 'Activated Carbon Block Filter (CTO 10-inch)', 'Appliance AMC', 64, 'blocks', 'Wing A & B', 'Chlorine, VOC and odor reduction filter'),
          ('SOCIETY_BULK', 1, '75 GPD Thin Film Composite (TFC) RO Membrane', 'Appliance AMC', 48, 'membranes', 'Wing A & B', 'High rejection desalting reverse osmosis membrane');
      `);
      console.log('Society bulk work items seeded for Service 1');
    }
  } catch (err) {
    console.error('Seed error:', err);
  } finally {
    await pool.end();
  }
}

seed();
