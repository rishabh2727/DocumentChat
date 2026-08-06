from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials, APIClient
from config.settings import settings
import re
import logging

logger = logging.getLogger(__name__)
credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                  )
client = APIClient(credentials)

# Temperature 0 means deterministic, no creative variation,
# since this is a classification task, not writing.
# I have max tokens 10 because the only valid output is one short word.
class RelevanceChecker:
    def __init__(self):
        self.model = ModelInference(
            model_id="ibm/granite-3-3-8b-instruct",
            credentials=credentials,
            project_id="skills-network",
            params={"temperature": 0, "max_tokens": 10},
        )
    
    def check(self,question, retriever,k=3):
        logger.debug(f"RelevanceChecker.check called with question='{question}' and k={k}")
        top_documents = retriever.invoke(question)
        if not top_documents:
            logger.debug("No Documents returned from retriever.invoke(), so nothing matches the question provided.")
            return "NO_DOCUMENTS_MATCHED"
        
        
                         
        
        
        
    