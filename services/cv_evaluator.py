from langchain_openai import ChatOpenAI

from models.cv_model import CVAnalysis
from prompts.cv_prompts import create_system_prompts
from services.config import *

from dotenv import load_dotenv
import os

load_dotenv()

class CVEvaluator:
    
    def __init__(self):
        self.model = self.create_cv_evaluator_model()
        self.chain = self._create_chain()

    def create_cv_evaluator_model(self):
        base_model = ChatOpenAI(
            api_key= os.getenv("API_KEY"),
            model = MODEL,
            temperature = TEMPERATURE,
        )
        
        structured_model = base_model.with_structured_output(CVAnalysis)
        
        return structured_model
    
    def _create_chain(self):
        chat_prompt = create_system_prompts()
        chain_evaluation = chat_prompt | self.model
        return chain_evaluation
        

    def evaluate_candidate(self, cv_text: str, job_description: str) -> CVAnalysis:
        try:
            chain_evaluation = self.chain
            
            result = chain_evaluation.invoke({
                "cv_text": cv_text,
                "job_description": job_description
            })
            
            return result
        
        except Exception as e:
            raise e
    
    @staticmethod
    def _error_response() -> CVAnalysis:
        return CVAnalysis(
                candidate_name = "Processing error.",
                years_experience = 0,
                key_skills = ["Error processing CV."],
                education = "Can not be determined.",
                relevant_experience = "Error during analysis.",
                strenghts = ["Requires manual CV review."],
                improvement_areas = ["Check the format and readability of the PDF."],
                adjustment_percentage = 0
            )