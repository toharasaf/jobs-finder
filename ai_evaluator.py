import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, CV_PATH

class AIEvaluator:
    def __init__(self):
        if GEMINI_API_KEY:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.client = None
            
        self.cv_text = self._load_cv()

    def _load_cv(self):
        try:
            with open(CV_PATH, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: CV file '{CV_PATH}' not found. Please create it and paste your CV.")
            return ""

    def evaluate_job(self, job_title: str, job_description: str) -> dict:
        """
        Evaluates if the job is a student job AND fits the CV.
        Returns a dictionary with 'Match' (bool) and 'Reason' (str).
        """
        if not self.client:
            print("Gemini API Key missing. Skipping AI evaluation.")
            return {"Match": False, "Reason": "API Key missing"}
            
        if not self.cv_text:
            print("CV text is empty. Skipping AI evaluation.")
            return {"Match": False, "Reason": "CV missing"}

        import datetime
        current_date = datetime.datetime.now().strftime("%B %Y")
        
        prompt = f"""
        You are an expert technical recruiter and ATS Optimizer. I am looking for a student job that fits my CV.
        
        IMPORTANT CONTEXT: 
        Today's date is {current_date}. Keep this in mind when calculating my years of study or experience based on the dates in my CV.
        
        My CV:
        {self.cv_text}
        
        Job Title: {job_title}
        Job Description:
        {job_description}
        
        Please evaluate this job based on two criteria:
        1. Is it a relevant student job? (It MUST be a student position, intern, or part-time in Electrical Engineering, Computer Engineering, or Software). If it is for Industrial Engineering, HR, or non-engineering, it is NOT relevant.
        2. ATS Match Percentage: Grade my CV against the job requirements from 0 to 100.
        
        Additionally, you must rewrite my CV to perfectly tailor it to this job's keywords and requirements to pass an ATS scan. Do NOT lie or invent experience I don't have, but DO change the phrasing of my existing experience to match the exact terms used in the Job Description.

        Return your answer ONLY as a valid JSON object with the following fields:
        - "IsRelevantDomain": true if it is a relevant engineering student job, false otherwise.
        - "MatchPercentage": an integer between 0 and 100 representing how well my original CV matches the requirements.
        - "Reason": A short sentence in Hebrew explaining the match percentage, what I'm missing, or why I was rejected.
        - "TailoredCV": A string containing my full, rewritten, and ATS-optimized CV in English.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            
            # Parse the JSON response
            result_text = response.text
            result = json.loads(result_text)
            
            # Ensure required keys exist
            if not all(key in result for key in ["IsRelevantDomain", "MatchPercentage", "Reason", "TailoredCV"]):
                return {"IsRelevantDomain": False, "MatchPercentage": 0, "Reason": "Invalid AI response structure"}
                
            return result
            
        except Exception as e:
            print(f"Error during AI evaluation: {e}")
            return {"IsRelevantDomain": False, "MatchPercentage": 0, "Reason": f"Error: {str(e)}", "Error": True}
