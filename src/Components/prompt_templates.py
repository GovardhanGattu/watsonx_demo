
def incident_analyser_prompt():
    prompt_template = """
        Provide me the answer along with incident numbers from Number column and 
        knowledge base article from the Description column.
        context: {context}
        input: {input}
        """

    return prompt_template
    

def data_analytics_prompt():
    prompt_template="""
        You are a Data Analyst, Your job is to answer my questions.
        provide me the best possible answer in a simple and  user readable
        based on the given input context.
        context: {context}
        input: {input}
        """

    return prompt_template
