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

        prompt = f"""
        You are an expert technical recruiter. I am looking for a student job that fits my CV.
        
        My CV:
        {self.cv_text}
        
        Job Title: {job_title}
        Job Description:
        {job_description}
        
        Please evaluate this job based on two criteria:
        1. Is it a student job? (It MUST be a student position, intern, or explicitly mention part-time/student suitability).
        2. Does it technically match the skills and experience in my CV?
        
        Return your answer ONLY as a valid JSON object with two fields:
        - "Match": true if both criteria are met, false otherwise.
        - "Reason": A short sentence in Hebrew explaining why it is a match or why it was rejected.
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
            if "Match" not in result or "Reason" not in result:
                return {"Match": False, "Reason": "Invalid AI response structure"}
                
            return result
            
        except Exception as e:
            print(f"Error during AI evaluation: {e}")
            return {"Match": False, "Reason": f"Error: {str(e)}", "Error": True}
