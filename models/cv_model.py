from pydantic import BaseModel, Field

class CVAnalysis(BaseModel):
    """Data model for full CV analysis"""
    candidate_name: str = Field(description="Candidate's full name extracted from CV.")
    years_experience: int = Field(description="Total years of relevant experience.")
    key_skills: list[str] = Field(description="List 5-7 most relevant candidate skills for the position.")
    education: str = Field(description="higher educational level and main specialization")
    relevant_experience: str = Field(description="Concise summary of the most relevant experience for the specific position.")
    strenghts: list[str] = Field(description="3-5 candidate strenghts based on their profile.")
    improvement_areas: list[str] = Field(description="2-4 areas in which the candidate could develop or improve.")
    adjustment_percentage: int = Field(description="Percentage of fit to the position (0-100) based on experience, skills, and education.", ge=0, le=100)