#!/usr/bin/env python3
"""
Database Setup Script for PM Internship Recommendation System
This script helps set up the Supabase database with all required tables and functions
"""

import os
import asyncio
from supabase_client import supabase_client

async def setup_database():
    """Set up the database with all required tables and functions"""
    
    print("🚀 Setting up PM Internship Recommendation System Database")
    print("=" * 60)
    
    # Check if Supabase is connected
    if not supabase_client.is_connected():
        print("❌ Supabase not connected. Please check your environment variables:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_ANON_KEY")
        print("\nMake sure to create a .env file with these variables.")
        return False
    
    print("✅ Supabase connected successfully")
    
    # Create tables and functions
    try:
        print("\n📋 Creating database schema...")
        
        # Read the SQL schema file
        with open('supabase_schema.sql', 'r') as f:
            sql_content = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            if statement:
                try:
                    # Execute the statement
                    result = supabase_client.client.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"✅ Statement {i+1}/{len(statements)} executed successfully")
                except Exception as e:
                    print(f"⚠️ Statement {i+1} failed (this might be expected if table already exists): {e}")
        
        print("\n✅ Database schema setup completed")
        
        # Test the setup by checking if we can access the tables
        print("\n🧪 Testing database setup...")
        
        # Test applications table
        try:
            result = supabase_client.client.table('applications').select('*').limit(1).execute()
            print("✅ Applications table accessible")
        except Exception as e:
            print(f"❌ Applications table error: {e}")
        
        # Test users table
        try:
            result = supabase_client.client.table('users').select('*').limit(1).execute()
            print("✅ Users table accessible")
        except Exception as e:
            print(f"❌ Users table error: {e}")
        
        # Test feedback table
        try:
            result = supabase_client.client.table('feedback').select('*').limit(1).execute()
            print("✅ Feedback table accessible")
        except Exception as e:
            print(f"❌ Feedback table error: {e}")
        
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Start the Flask backend: python app.py")
        print("2. Build and start the frontend: cd twin-digital-copy-main/twin-digital-copy-main && npm run build && npm run dev")
        print("3. Access the application at http://localhost:5000")
        print("4. Use the navigation to switch between Candidate View, Recruiter Dashboard, and Feedback & Learning")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def main():
    """Main function"""
    print("PM Internship Recommendation System - Database Setup")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️ .env file not found. Creating template...")
        with open('.env', 'w') as f:
            f.write("""# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# OpenAI Configuration (for RAG system)
OPENAI_API_KEY=your_openai_api_key_here
""")
        print("✅ Created .env template. Please fill in your actual values.")
        return
    
    # Run the setup
    asyncio.run(setup_database())

if __name__ == "__main__":
    main()
