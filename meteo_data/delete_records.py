#!/usr/bin/env python3
"""
Delete Records Script for Weather Database
Erases all data from the weather_data.db SQLite database
"""

import sqlite3
import os
import logging
from datetime import datetime
from .config import DATABASE_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseCleaner:
    def __init__(self, db_path: str = None):
        """Initialize the database cleaner with database path"""
        self.db_path = db_path or DATABASE_PATH
    
    def check_database_exists(self):
        """Check if the database file exists"""
        return os.path.exists(self.db_path)
    
    def get_record_count(self):
        """Get the current number of records in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error getting record count: {e}")
            return None
    
    def delete_all_records(self):
        """Delete all records from the weather_data table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete all records from weather_data table
            cursor.execute("DELETE FROM weather_data")
            
            # Reset the auto-increment counter
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='weather_data'")
            
            conn.commit()
            conn.close()
            
            logger.info("All records have been successfully deleted from the database")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting records: {e}")
            return False
    
    def vacuum_database(self):
        """Vacuum the database to reclaim space after deletion"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("VACUUM")
            conn.close()
            logger.info("Database has been vacuumed to reclaim space")
        except Exception as e:
            logger.error(f"Error vacuuming database: {e}")

def main():
    """Main function to delete all records"""
    cleaner = DatabaseCleaner()
    
    # Check if database exists
    if not cleaner.check_database_exists():
        logger.warning(f"Database file '{cleaner.db_path}' does not exist")
        return
    
    # Get current record count
    record_count = cleaner.get_record_count()
    if record_count is None:
        logger.error("Could not determine record count. Exiting.")
        return
    
    if record_count == 0:
        logger.info("Database is already empty. No records to delete.")
        return
    
    logger.info(f"Found {record_count} records in the database")
    
    # Confirm deletion
    print(f"\nWARNING: This will permanently delete all {record_count} records from the weather database!")
    print(f"Database file: {cleaner.db_path}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    confirmation = input("\nAre you sure you want to proceed? Type 'YES' to confirm: ")
    
    if confirmation != 'YES':
        logger.info("Operation cancelled by user")
        return
    
    # Delete all records
    logger.info("Starting deletion process...")
    success = cleaner.delete_all_records()
    
    if success:
        # Vacuum database to reclaim space
        cleaner.vacuum_database()
        
        # Verify deletion
        final_count = cleaner.get_record_count()
        if final_count == 0:
            logger.info("✅ All records have been successfully deleted!")
            logger.info("Database is now empty and ready for new data collection")
        else:
            logger.warning(f"⚠️  Deletion may not have been complete. {final_count} records remain")
    else:
        logger.error("❌ Failed to delete records")

if __name__ == "__main__":
    main()