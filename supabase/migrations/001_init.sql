-- Create customers table
create table public.customers (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  name text,
  phone text,
  company_name text,
  created_at timestamptz default now()
);

-- Create orders table
create table public.orders (
  id uuid primary key default gen_random_uuid(),
  order_number bigint not null unique,
  customer_id uuid references public.customers(id) on delete cascade, --delete all child rows if parent row is deleted
  created_date text,
  created_time text,
  total_quantity int,
  payment_status text,
  payment_method text,
  coupon_code text,
  gift_card_amt numeric,
  shipping_rate numeric,
  total_tax numeric,
  total numeric,
  currency text,
  refunded_amt numeric,
  net_amt numeric,
  fulfillment_status text,
  note text,
  additional_info text,
  wix_order_id text unique, -- will be used when real-time Wix data is added
  created_at timestamptz default now()
);

-- Create order_items table
create table public.order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid references public.orders(id) on delete cascade,
  item text,
  variant text,
  sku text,
  qty int,
  qty_refunded int,
  price numeric,
  weight numeric,
  custom_text text,
  deposit_amt numeric
);

-- Create shipping_addresses table
create table public.shipping_addresses (
  id uuid primary key default gen_random_uuid(),
  order_id uuid references public.orders(id) on delete cascade,
  recipient_phone text,
  company_name text,
  country text,
  state text,
  city text,
  address text,
  postal_code text,
  delivery_method text,
  delivery_item text
);

-- Create billing_addresses table
create table public.billing_addresses (
  id uuid primary key default gen_random_uuid(),
  order_id uuid references public.orders(id) on delete cascade,
  name text,
  phone text,
  company_name text,
  country text,
  state text,
  city text,
  address text,
  postal_code text
);

-- Create fulfillments table
create table public.fulfillments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid references public.orders(id) on delete cascade,
  tracking_number text,
  service text,
  shipping_label text
);