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
from scrapers.arm_scraper import ArmScraper
from scrapers.ceva_scraper import CevaScraper
from scrapers.sandisk_scraper import SanDiskScraper

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
        WorkdayScraper(tenant="broadcom", site="External_Career", company="Broadcom", location_facets=["2314daa817fc016cb4c254532e010de8"]),
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
        ArmScraper(),
        CevaScraper(),
        SanDiskScraper(),
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
                
                # FALLBACK: If AI hits the 20-request daily quota, don't throw the job away. 
                if evaluation.get("Error") and "429" in evaluation.get("Reason", ""):
                    print("AI Quota hit! Sending job to Telegram as a fallback without AI filter...")
                    evaluation = {
                        "IsRelevantDomain": True,
                        "MatchPercentage": 100, 
                        "Reason": "⚠️ ה-AI מיצה את 20 הבקשות היומיות שלו של גוגל. המשרה נשלחת אלייך על בסיס סינון מילות מפתח (סטודנט) כדי שלא תפספס אותה!",
                        "TailoredCV": ""
                    }
                
                # 6. Send notification if it is a relevant domain
                if evaluation.get("IsRelevantDomain"):
                    match_pct = evaluation.get("MatchPercentage", 0)
                    reason = evaluation.get("Reason", "")
                    tailored_cv = evaluation.get("TailoredCV", "")
                    
                    # Choose emoji based on score
                    emoji = "🎯" if match_pct >= 80 else "⚠️"
                    
                    message = (
                        f"{emoji} *משרה רלוונטית חדשה! (התאמה: {match_pct}%)*\n\n"
                        f"🔹 *תפקיד:* {job.title}\n"
                        f"🏢 *חברה:* {job.company}\n"
                        f"💡 *ניתוח ה-AI:* {reason}\n\n"
                        f"🔗 [קישור למשרה]({job.url})"
                    )
                    
                    if tailored_cv:
                        # Write tailored CV to PDF file
                        cv_filename = "Tohar_Asaf_CV.pdf"
                        import os
                        from pdf_generator import create_cv_pdf
                        
                        pdf_success = create_cv_pdf(tailored_cv, cv_filename)
                        
                        if pdf_success:
                            # Send the PDF document with the message as caption
                            from telegram_notifier import send_telegram_document
                            send_telegram_document(cv_filename, caption=message)
                            
                            # Clean up the temp file
                            try:
                                os.remove(cv_filename)
                            except:
                                pass
                        else:
                            # Fallback to standard message if PDF generation fails
                            from telegram_notifier import send_telegram_message
                            send_telegram_message(message)
                    else:
                        from telegram_notifier import send_telegram_message
                        send_telegram_message(message)
                
                # 7. Mark as seen in DB so we don't process it again
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
