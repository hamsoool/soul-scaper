import asyncio
import logging
import sys

from app.database import async_session
from app.scraper import sync_doe_data

# Configure stdout logging to see progress
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)

async def main():
    print("==============================================================")
    print("  Starting Local Scraper Sync Session against Supabase...")
    print("==============================================================")
    
    async with async_session() as session:
        try:
            result = await sync_doe_data(session)
            print("\n==============================================================")
            print("  Sync Execution Finished successfully!")
            print("==============================================================")
            print(f"Status:          {result['status']}")
            print(f"Processed:       {result['processed_count']} new PDF(s)")
            print(f"Time Taken:      {result['duration_seconds']:.2f} seconds")
            if result['errors']:
                print("\nEncountered Errors:")
                for err in result['errors']:
                    print(f" - {err}")
            print("==============================================================")
        except Exception as e:
            print("\nFatal Error occurred during execution:")
            print(e)
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
