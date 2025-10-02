import { createClient } from '@supabase/supabase-js'
// Create a single supabase client for interacting with your database

const url = 'https://nfagjkycxmwznywezuke.supabase.co'
const anon = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYWdqa3ljeG13em55d2V6dWtlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcxNDQ0NTksImV4cCI6MjA3MjcyMDQ1OX0.Z5YsrVPw_rj51EBfW38BKa8c39s5B3d07RlZqnhSK7o'
export const supabase = createClient(url, anon)
