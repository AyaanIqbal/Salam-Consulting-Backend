-- Enable Row Level Security on all relevant tables
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE stages ENABLE ROW LEVEL SECURITY;
ALTER TABLE flags ENABLE ROW LEVEL SECURITY;

-- Allow full access to service_role for customers
CREATE POLICY "Service Role Full Access - customers"
  ON customers
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Allow full access to service_role for orders
CREATE POLICY "Service Role Full Access - orders"
  ON orders
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Allow full access to service_role for stages
CREATE POLICY "Service Role Full Access - stages"
  ON stages
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Allow full access to service_role for flags
CREATE POLICY "Service Role Full Access - flags"
  ON flags
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
