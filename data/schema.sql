-- ============================================================
-- PropAgent — Supabase SQL Schema
-- Run this in the Supabase SQL editor to initialize all tables
-- ============================================================

-- PROFILES — one row per authenticated user
CREATE TABLE IF NOT EXISTS profiles (
  id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name  TEXT,
  last_name   TEXT,
  email       TEXT UNIQUE NOT NULL,
  phone       TEXT,
  role        TEXT NOT NULL DEFAULT 'seller',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- LISTINGS — property listings created by sellers
CREATE TABLE IF NOT EXISTS listings (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  address        TEXT NOT NULL,
  city           TEXT,
  state          TEXT,
  zip            TEXT,
  price          NUMERIC,
  bedrooms       INTEGER,
  bathrooms      NUMERIC,
  sqft           INTEGER,
  lot_size       INTEGER,
  year_built     INTEGER,
  property_type  TEXT NOT NULL DEFAULT 'single_family',
  status         TEXT NOT NULL DEFAULT 'draft',  -- draft | live | pending | sold
  description    TEXT,
  commission     NUMERIC NOT NULL DEFAULT 2.5,   -- buyer's agent commission %
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- SHOWINGS — individual showing requests tied to a listing
CREATE TABLE IF NOT EXISTS showings (
  id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id             UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  user_id                UUID NOT NULL REFERENCES profiles(id),
  buyer_name             TEXT,
  buyer_agent            TEXT,
  buyer_agent_brokerage  TEXT,
  showing_date           DATE,
  showing_time           TIME,
  duration_minutes       INTEGER NOT NULL DEFAULT 30,
  status                 TEXT NOT NULL DEFAULT 'pending',  -- pending | confirmed | cancelled
  notes                  TEXT,
  created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- APPOINTMENTS — any scheduled event for a listing (showing, inspection, photography, etc.)
CREATE TABLE IF NOT EXISTS appointments (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id       UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  user_id          UUID NOT NULL REFERENCES profiles(id),
  type             TEXT NOT NULL,   -- showing | inspection | photography | appraisal | other
  title            TEXT,
  scheduled_at     TIMESTAMPTZ,
  duration_minutes INTEGER NOT NULL DEFAULT 60,
  status           TEXT NOT NULL DEFAULT 'scheduled',  -- scheduled | completed | cancelled
  contact_name     TEXT,
  contact_phone    TEXT,
  notes            TEXT,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ACTIVITY — audit log / feed of events per user
CREATE TABLE IF NOT EXISTS activity (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES profiles(id),
  listing_id  UUID REFERENCES listings(id) ON DELETE SET NULL,
  type        TEXT,    -- listing_created | showing_request | offer_received | price_changed | etc.
  message     TEXT NOT NULL,
  color       TEXT NOT NULL DEFAULT 'blue',  -- green | blue | gold | accent
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- PRICE_ANALYSIS — weekly automated price analysis reports
CREATE TABLE IF NOT EXISTS price_analysis (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id          UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  run_date            DATE NOT NULL,
  verdict             TEXT,   -- price_reduction | on_target | underpriced
  current_price       NUMERIC,
  recommended_price   NUMERIC,
  median_comp_price   NUMERIC,
  analysis_text       TEXT,
  comps               JSONB,  -- array of comparable sale objects
  accepted            BOOLEAN NOT NULL DEFAULT FALSE,
  dismissed           BOOLEAN NOT NULL DEFAULT FALSE,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE profiles      ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings      ENABLE ROW LEVEL SECURITY;
ALTER TABLE showings      ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments  ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity      ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_analysis ENABLE ROW LEVEL SECURITY;

-- profiles
CREATE POLICY "profiles_select_own" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "profiles_insert_own" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update_own" ON profiles FOR UPDATE USING (auth.uid() = id);

-- listings
CREATE POLICY "listings_select_own" ON listings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "listings_insert_own" ON listings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "listings_update_own" ON listings FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "listings_delete_own" ON listings FOR DELETE USING (auth.uid() = user_id);

-- showings
CREATE POLICY "showings_select_own" ON showings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "showings_insert_own" ON showings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "showings_update_own" ON showings FOR UPDATE USING (auth.uid() = user_id);

-- appointments
CREATE POLICY "appointments_select_own" ON appointments FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "appointments_insert_own" ON appointments FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "appointments_update_own" ON appointments FOR UPDATE USING (auth.uid() = user_id);

-- activity
CREATE POLICY "activity_select_own" ON activity FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "activity_insert_own" ON activity FOR INSERT WITH CHECK (auth.uid() = user_id);

-- price_analysis (scoped through listings ownership)
CREATE POLICY "price_analysis_select_own" ON price_analysis FOR SELECT USING (
  listing_id IN (SELECT id FROM listings WHERE user_id = auth.uid())
);
CREATE POLICY "price_analysis_insert_own" ON price_analysis FOR INSERT WITH CHECK (
  listing_id IN (SELECT id FROM listings WHERE user_id = auth.uid())
);
CREATE POLICY "price_analysis_update_own" ON price_analysis FOR UPDATE USING (
  listing_id IN (SELECT id FROM listings WHERE user_id = auth.uid())
);

-- ============================================================
-- AUTO-UPDATE updated_at TRIGGER
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at  BEFORE UPDATE ON profiles  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER listings_updated_at  BEFORE UPDATE ON listings  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
