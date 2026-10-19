-- ============================================================================
-- SocietySync — Schema Extensions for Work Items, Facilities, Chat & 2-Hour Auto-Assign
-- ============================================================================

-- 1. COMMON FACILITIES TABLE (Society Common Equipment & Assets)
CREATE TABLE IF NOT EXISTS society_facilities (
    id SERIAL PRIMARY KEY,
    society_id INT NOT NULL REFERENCES societies(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    wing VARCHAR(100) DEFAULT 'All Wings',
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. DYNAMIC WORK ITEMS TABLE (Itemized Breakdown for Society & Resident Work Requests)
CREATE TABLE IF NOT EXISTS work_request_items (
    id SERIAL PRIMARY KEY,
    request_type VARCHAR(20) NOT NULL CHECK (request_type IN ('SOCIETY_BULK', 'FLAT_MAINTENANCE')),
    request_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit VARCHAR(50) DEFAULT 'units',
    wing_flat_reference VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_work_items_req ON work_request_items(request_type, request_id);

-- 3. RESIDENCE CONVERSATIONS (Distinct Worker-Resident Chat Channels)
CREATE TABLE IF NOT EXISTS residence_conversations (
    id SERIAL PRIMARY KEY,
    work_request_id INT REFERENCES flat_maintenance_requests(id) ON DELETE CASCADE,
    resident_user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    worker_user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(30) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'CLOSED', 'ARCHIVED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(work_request_id, resident_user_id, worker_user_id)
);

CREATE INDEX IF NOT EXISTS idx_conv_users ON residence_conversations(resident_user_id, worker_user_id);

-- 4. CHAT MESSAGES TABLE
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL REFERENCES residence_conversations(id) ON DELETE CASCADE,
    sender_user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_conv ON chat_messages(conversation_id, created_at);

-- 5. AUTO-ASSIGNMENT AUDIT LOG TABLE
CREATE TABLE IF NOT EXISTS auto_assignment_logs (
    id SERIAL PRIMARY KEY,
    request_id INT NOT NULL REFERENCES flat_maintenance_requests(id) ON DELETE CASCADE,
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    elapsed_minutes INT NOT NULL,
    result_status VARCHAR(50) NOT NULL, -- 'AUTO_ASSIGNED', 'NEEDS_MANUAL_ASSIGNMENT', 'SKIPPED_ALREADY_CLAIMED'
    matched_worker_id INT REFERENCES worker_profiles(id),
    reason TEXT NOT NULL
);

-- 6. PERSISTENT SERVERLESS EMAIL OTPS TABLE
CREATE TABLE IF NOT EXISTS email_otps (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    purpose VARCHAR(100),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_email_otps_lookup ON email_otps (email, otp_code);

