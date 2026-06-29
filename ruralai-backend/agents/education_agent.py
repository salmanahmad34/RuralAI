from typing import Dict, List, Any, Optional
import logging
import json
import re
from mcp_servers.education_mcp import EducationMCPServer

class EducationAgent:
    """Agent resolving academic scholarship searches, school locations, eligibility conditions, and career advice."""

    def __init__(self, education_mcp: EducationMCPServer, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.education_mcp = education_mcp
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("EducationAgent")

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's education query. Identify intent, trigger education MCP, compile recommendations."""
        self.logger.info(f"EducationAgent processing query: '{query}'")
        
        parsed = await self._parse_education_parameters(query)
        intent = parsed.get("intent", "scholarship_finder")
        age = parsed.get("age", 15)
        grade = parsed.get("grade", "10")
        annual_income = parsed.get("annual_income", 150000.0)
        caste = parsed.get("caste", "All")
        state = parsed.get("state", "Maharashtra")
        scheme_id = parsed.get("scheme_id", "pm_scholarship")
        interests = parsed.get("interests", ["agriculture"])
        lat = parsed.get("lat", 18.5204)
        lon = parsed.get("lon", 73.8567)

        recommendations = []
        sources = ["EducationMCPServer"]

        try:
            if intent == "school_finder" or any(w in query.lower() for w in ["school", "college", "admission", "study center"]):
                schools = await self.education_mcp.find_nearby_schools(lat, lon, grade=grade)
                sources.append("EducationMCPServer (Geographic School Search)")
                
                desc_lines = []
                for s in schools:
                    desc_lines.append(f"- {s['name']} ({s['distance_km']} km away): Type: {s['type']}, Grades: {', '.join(s['grades'])}, Contact: {s['contact']}")
                    
                recommendations.append({
                    "title": f"Nearby Schools & Colleges (within 20km radius)",
                    "description": "\n".join(desc_lines) if desc_lines else "No government schools found within 20km matching requirements.",
                    "source": "EducationMCP",
                    "confidence": 0.95
                })

            elif intent == "eligibility_checker" or any(w in query.lower() for w in ["eligible", "check eligibility", "qualify"]):
                profile = {
                    "age": age,
                    "grade": grade,
                    "annual_income": annual_income,
                    "caste": caste,
                    "state": state
                }
                eligibility = await self.education_mcp.check_scholarship_eligibility(scheme_id, profile)
                sources.append("EducationMCPServer (Eligibility Verification Engine)")
                
                status_str = "Eligible" if eligibility["eligible"] else "Not Eligible"
                reasons_str = "; ".join(eligibility["reasons"])
                docs_str = ", ".join(eligibility["missing_documents"])
                
                desc = f"Eligibility Status: **{status_str}**. Breakdown: {reasons_str}. "
                if eligibility["eligible"]:
                    desc += f"Please gather the following documents to apply: {docs_str}."
                else:
                    desc += "Please verify your parameters and check other schemes."
                    
                recommendations.append({
                    "title": f"Eligibility Verification for Scheme: {scheme_id.title()}",
                    "description": desc,
                    "source": "EducationMCP",
                    "confidence": 0.98
                })

            elif intent == "career_guidance" or any(w in query.lower() for w in ["career", "job", "what to do", "guidance", "interest"]):
                guidance = await self.education_mcp.get_career_guidance(int(grade) if grade.isdigit() else 10, interests)
                sources.append("EducationMCPServer (Career Paths)")
                
                desc_lines = []
                for c in guidance["career_options"]:
                    desc_lines.append(f"**{c['career']}**:\n  - Path: {c['path']}\n  - Top Institutes: {c['institutes']}")
                desc_lines.append(f"\nGeneral Advice: {guidance['general_advice']}")
                
                recommendations.append({
                    "title": f"Career Guidance Report based on Interests: {', '.join(interests)}",
                    "description": "\n".join(desc_lines),
                    "source": "EducationMCP",
                    "confidence": 0.85
                })

            else:
                # Default: Scholarship Finder
                profile = {
                    "age": age,
                    "grade": grade,
                    "annual_income": annual_income,
                    "caste": caste,
                    "state": state
                }
                scholarships = await self.education_mcp.get_eligible_scholarships(profile)
                sources.append("EducationMCPServer (Scholarship Database)")
                
                desc_lines = []
                for s in scholarships:
                    desc_lines.append(f"- **{s['name']}** (ID: {s['id']}): Amount: {s['amount_annual']} INR/year. Apply by: {s['deadline']}. Authority: {s['authority']} (Match Score: {s['match_score']})")
                    
                recommendations.append({
                    "title": f"Eligible Government Scholarship Opportunities",
                    "description": "\n".join(desc_lines) if desc_lines else "No matching scholarships found for this profile. Try checking income/caste inputs.",
                    "source": "EducationMCP",
                    "confidence": 0.90
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Educational Database Support Error",
                "description": "Unable to execute educational lookup. Please verify inputs (grade, caste, state) and try again.",
                "source": "EducationAgent",
                "confidence": 0.50
            })

        return {
            "agent": "education",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_education_parameters(self, query: str) -> Dict[str, Any]:
        """Extract educational profiles (grade, income, caste, state, interests) from query."""
        params = {
            "intent": "scholarship_finder",
            "age": 15,
            "grade": "10",
            "annual_income": 150000.0,
            "caste": "All",
            "state": "Maharashtra",
            "scheme_id": "pm_scholarship",
            "interests": ["agriculture"],
            "lat": 18.5204,
            "lon": 73.8567
        }
        
        ql = query.lower()
        
        # Check intents
        if any(w in ql for w in ["school", "college", "admission", "study center"]):
            params["intent"] = "school_finder"
        elif any(w in ql for w in ["eligible", "qualify", "check eligibility"]):
            params["intent"] = "eligibility_checker"
        elif any(w in ql for w in ["career", "job", "future", "work", "guidance", "interest"]):
            params["intent"] = "career_guidance"

        if self.llm_client:
            prompt = (
                "Extract education profile parameters from this user query. Return a valid JSON object matching this schema:\n"
                '{"intent": "scholarship_finder"|"school_finder"|"eligibility_checker"|"career_guidance", '
                '"age": integer, "grade": "string (e.g. 8, 9, 10, 11, 12, Graduate)", "annual_income": float, '
                '"caste": "All"|"OBC"|"SC"|"ST", "state": "string (Indian state)", '
                '"scheme_id": "string (scholarship ID if mentioned)", "interests": ["string (e.g. teaching, agriculture, technology)"], '
                '"lat": float, "lon": float}\n'
                f"Query: '{query}'"
            )
            try:
                if self.llm_provider == "google":
                    response = self.llm_client.generate_content(prompt)
                    data = json.loads(re.sub(r'```json|```', '', response.text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                elif self.llm_provider == "anthropic":
                    response = await self.llm_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=250,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content_text = response.content[0].text
                    data = json.loads(re.sub(r'```json|```', '', content_text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                return params
            except Exception as e:
                self.logger.warning(f"LLM extraction failed, using fallback regex parser: {e}")

        # Fallback regex parser
        castes = ["obc", "sc", "st"]
        for c in castes:
            if c in ql:
                params["caste"] = c.upper()
                break
                
        grade_match = re.search(r'\b(grade|class|standard|std)\s*(\d+)\b', ql)
        if grade_match:
            params["grade"] = grade_match.group(2)
        else:
            # direct numbers checking
            for g in ["9", "10", "11", "12"]:
                if f" {g}th" in ql or f" {g} class" in ql:
                    params["grade"] = g
                    break
                    
        states = ["maharashtra", "karnataka", "tamil nadu", "rajasthan", "punjab"]
        for s in states:
            if s in ql:
                params["state"] = s.title()
                break
                
        # Income check
        income_match = re.search(r'\b(income|salary)\s*(of|is)?\s*(\d+)\b', ql)
        if income_match:
            params["annual_income"] = float(income_match.group(3))
            
        # Interests extraction
        interests_list = ["agriculture", "technology", "teaching", "medical", "computer"]
        found_interests = []
        for i in interests_list:
            if i in ql:
                found_interests.append(i)
        if found_interests:
            params["interests"] = found_interests
            
        return params
