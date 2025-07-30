-- Create stage_name_enum safely
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stage_name_enum') THEN
    CREATE TYPE stage_name_enum AS ENUM (
      'discovery_call',
      'resume_review',
      'career_coaching',
      'interview_prep',
      'custom_service'
    );
  END IF;
END$$;

-- Create flag_type_enum safely
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'flag_type_enum') THEN
    CREATE TYPE flag_type_enum AS ENUM (
      'blocked',
      'needs_help',
      'manual_check',
      'no_recent_checkin',
      'stuck_in_stage',
      'missing_info'
    );
  END IF;
END$$;

-- Create stages table
CREATE TABLE IF NOT EXISTS stages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid REFERENCES customers(id) ON DELETE CASCADE,
  stage_name stage_name_enum NOT NULL,
  entered_at timestamptz NOT NULL DEFAULT now(),
  is_active boolean NOT NULL DEFAULT true
);

-- Create flags table
CREATE TABLE IF NOT EXISTS flags (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid REFERENCES customers(id) ON DELETE CASCADE,
  flag_type flag_type_enum NOT NULL,
  flagged_at timestamptz NOT NULL DEFAULT now(),
  notes text
);
