from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials, APIClient
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

        # top_documents are list of document objects that has its own page_content, metadata.
        # pulling just the text out of each Document and gluing them together
        # with blank lines between them, so the model can read them as separate passages
        # rather than one run-on block.
        # we have to flatten the list of chunk objects that is top_documents into a string
        # since an LLM API can only take a block of text as input. 

        combine_k_chunks = "\n\n".join(chunk.page_content for chunk in top_documents[:k])
        
        # locking down exactly what answer we want, just one sentence
        #Clear labels like ** question ** so the ai is able to read what the instructions
        # are, what our prompts, so it does not get confused.
        # writing a clear prompt with instructions, labels,passing in the user question
        # and document content in curly brackets,
        prompt = f"""
        You are an AI relevance checker between a user's question and provided document content.

        **Instructions:**
        - Classify how well the document content addresses the user's question.
        - Respond with only one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH.
        - Do not include any additional text or explanation.

        **Labels:**
        1) "CAN_ANSWER": The passages contain enough explicit information to fully answer the question.
        2) "PARTIAL": The passages mention or discuss the question's topic but do not provide all the details needed for a complete answer.
        3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.

        **Important:** If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".

        **Question:** {question}
        **Passages:** {combine_k_chunks}

        **Respond ONLY with one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH**
        """
        
        # now we call the llm and see what the response is
        # calling the model, pulling the answer out of the response,
        # and making sure that answer is actually usable.
        try:
            response = self.model.chat(
                messages = [
                    {"role": "user",
                     "content": prompt
                    }
                ]
            )
        except Exception as e:
            logger.error("Error")
            return "No_MATCH"
        
        