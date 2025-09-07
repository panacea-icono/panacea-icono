#!/usr/bin/env python3
"""
⏰ Auto-Update Script for PANACEA ICONO Repository List
Automatically updates README.md with fresh repository data
Can be run as a cron job or scheduled task
"""

import os
import sys
import asyncio
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_readme import ReadmeGenerator


class AutoUpdater:
    """Automatic repository list updater"""
    
    def __init__(self, readme_file: str = "README.md"):
        self.readme_file = readme_file
        self.generator = ReadmeGenerator(readme_file)
        
    async def update(self, force_refresh: bool = True) -> bool:
        """Update the repository list"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"🕒 Starting auto-update at {timestamp}")
            
            # Update README
            success = await self.generator.update_readme()
            
            if success:
                logging.info("✅ Auto-update completed successfully")
                
                # Check if we're in a git repository
                if os.path.exists('.git'):
                    logging.info("🔍 Git repository detected - you may want to commit changes")
                    logging.info("💡 Run: git add README.md && git commit -m 'chore: auto-update repository list'")
                
                return True
            else:
                logging.error("❌ Auto-update failed")
                return False
                
        except Exception as e:
            logging.error(f"💥 Auto-update error: {e}")
            return False


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Auto-update PANACEA ICONO repository list"
    )
    parser.add_argument(
        "--readme", 
        default="README.md",
        help="Path to README.md file (default: README.md)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Show what would be updated without making changes"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    if args.dry_run:
        logging.info("🧪 DRY RUN MODE - No changes will be made")
        return 0
    
    print("🏥 PANACEA ICONO - Auto Repository List Updater")
    print("=" * 55)
    
    updater = AutoUpdater(args.readme)
    success = await updater.update()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)