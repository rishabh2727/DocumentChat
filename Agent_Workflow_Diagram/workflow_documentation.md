Workflow breakdown
Check relevance – The RelevanceChecker determines if the query can be answered based on the retrieved documents.

If relevant → Proceed to research

If irrelevant → Terminate workflow

Research step – The ResearchAgent generates a draft answer using relevant documents.

Verification step – The VerificationAgent assesses the draft answer for accuracy and relevance.

Decision making – Based on verification:

If the answer lacks support → Re-research and refine

If verified → End workflow