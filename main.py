import time
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from config import validate_config
from db import JobDB
from ai_evaluator import AIEvaluator
from telegram_notifier import send_telegram_message

# Import scrapers
from scrapers.workday_scraper import WorkdayScraper
from scrapers.mobileye_scraper import MobileyeScraper
from scrapers.oracle_scraper import OracleScraper
from scrapers.amazon_scraper import AmazonScraper
from scrapers.mprest_scraper import MPrestScraper
from scrapers.tomer_scraper import TomerScraper
from scrapers.xsight_scraper import XsightScraper
from scrapers.qualcomm_scraper import QualcommScraper
from scrapers.elbit_scraper import ElbitScraper
from scrapers.wix_scraper import WixScraper

def main():
    print("Starting Job Scraper Bot...")
    
    # 1. Validate configuration and keys
    try:
        validate_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        print("Please set up your .env file and try again.")
        return

    # 2. Initialize DB and AI
    db = JobDB()
    ai = AIEvaluator()
    
    # 3. Register scrapers
    scrapers = [
        WorkdayScraper(tenant="intel", site="External", company="Intel"),
        WorkdayScraper(tenant="marvell", site="MarvellCareers", company="Marvell"),
        WorkdayScraper(tenant="cadence", site="External_Careers", company="Cadence"),
        MobileyeScraper(),
        OracleScraper(
            api_url="https://iawmqy.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=CX_1",
            job_url_base="https://iawmqy.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/careers/job/",
            company="Rafael/Oracle"
        ),
        OracleScraper(
            api_url="https://edbz.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=CX",
            job_url_base="https://edbz.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/",
            company="Nova/OracleCloud"
        ),
        AmazonScraper(),
        MPrestScraper(),
        TomerScraper(),
        XsightScraper(),
        QualcommScraper(),
        ElbitScraper(),
        WixScraper(),
    ]
    
    # Polling loop (runs every 15 minutes)
    POLL_INTERVAL = 60 * 15  # 15 minutes in seconds

    while True:
        print(f"\n--- Starting scan at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        for scraper in scrapers:
            print(f"Scraping with {scraper.__class__.__name__}...")
            jobs = scraper.fetch_jobs()
            
            for job in jobs:
                # 4. Check if job was already processed
                if db.is_job_seen(job.id):
                    # print(f"Job {job.title} already processed. Skipping.")
                    continue
                    
                print(f"Found new job: {job.title} at {job.company}")
                
                # 5. Evaluate job using Gemini AI
                evaluation = ai.evaluate_job(job.title, job.description)
                print(f"AI Evaluation: {evaluation}")
                
                # 6. Send notification if it's a match
                if evaluation.get("Match"):
                    message = (
                        f"🎯 *התאמת משרה חדשה!*\n\n"
                        f"🔹 *תפקיד:* {job.title}\n"
                        f"🏢 *חברה:* {job.company}\n"
                        f"💡 *למה זה מתאים?* {evaluation.get('Reason')}\n\n"
                        f"🔗 [קישור למשרה]({job.url})"
                    )
                    send_telegram_message(message)
                
                # 7. Mark as seen in DB so we don't process it again (unless AI failed)
                if evaluation.get("Error"):
                    print("Skipping DB save due to AI error (will retry next scan).")
                else:
                    db.add_job(job.id)
                
                # Sleep briefly between AI calls to avoid hitting rate limits too fast
                time.sleep(5)
                
        print(f"Scan complete. Waiting {POLL_INTERVAL // 60} minutes for the next run...")
        try:
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nBot stopped manually.")
            break

if __name__ == "__main__":
    main()
